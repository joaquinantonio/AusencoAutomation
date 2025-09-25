import csv, json
from typing import List, Dict
from app.schemas.finance import FinanceReport, VarianceRow
from app.llm.client import get_client, DRY_RUN

def _read_gl(path:str)->List[Dict]:
    rows=[];
    with open(path,newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f):
            rows.append({"account":r.get("account","").strip(),
                         "actual":float(r.get("actual",0) or 0),
                         "budget":float(r.get("budget",0) or 0)})
    return rows

def _compute_variance(rows:List[Dict])->List[Dict]:
    out=[]
    for r in rows:
        b=r["budget"]; a=r["actual"]
        var=0.0 if b==0 else (a-b)/b*100.0
        out.append({"account":r["account"],"actual":a,"budget":b,"variance_pct":round(var,2)})
    return out

def _highlights(var_rows:List[Dict],n:int=3)->List[str]:
    tops=sorted(var_rows,key=lambda r:abs(r["variance_pct"]),reverse=True)[:n]
    return [f"{r['account']} {'over' if r['variance_pct']>0 else 'under'} budget by {abs(r['variance_pct']):.2f}% (Actual {r['actual']:.0f} vs Budget {r['budget']:.0f})" for r in tops]

def _risks(var_rows:List[Dict])->List[str]:
    rs=[]
    if any(r for r in var_rows if r["account"].lower().startswith("marketing") and r["variance_pct"]>10): rs.append("Marketing spend exceeds threshold (>10%).")
    if any(r for r in var_rows if r["account"].lower()=="cogs" and r["variance_pct"]<-5): rs.append("COGS materially under budget; verify allocations.")
    if not rs: rs.append("Monitor cash flow and receivables; variances within control limits.")
    return rs[:3]

def draft_finance_report(cfg:Dict)->Dict:
    period=cfg.get("period","2025-08"); rows=_read_gl(cfg["input_path"]); vars=_compute_variance(rows)
    if DRY_RUN or get_client() is None:
        table=sorted(vars,key=lambda r:abs(r["variance_pct"]),reverse=True)[:5]
        rep=FinanceReport(period, _highlights(vars,3), [VarianceRow(**r) for r in table], _risks(vars))
        return rep.to_json()
    client=get_client()
    messages=[{"role":"system","content":"Return only JSON for FinanceReport schema."},
              {"role":"user","content":json.dumps({"period":period,"gl":vars})}]
    schema={"type":"json_schema","json_schema":{"name":"FinanceReport","schema":{"type":"object",
            "required":["period","highlights","variance_table","risks"],
            "properties":{"period":{"type":"string"},"highlights":{"type":"array","items":{"type":"string"}},
                          "variance_table":{"type":"array","items":{"type":"object",
                            "required":["account","actual","budget","variance_pct"],
                            "properties":{"account":{"type":"string"},"actual":{"type":"number"},
                                          "budget":{"type":"number"},"variance_pct":{"type":"number"}}}},
                          "risks":{"type":"array","items":{"type":"string"}}}}}}
    resp=client.chat(messages,response_format=schema)
    content=resp["choices"][0]["message"]["content"]
    data=json.loads(content)
    assert data.get("period")
    return data
