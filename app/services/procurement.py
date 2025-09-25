import re, json
from typing import Dict, List
from app.llm.client import get_client, DRY_RUN

def _read(path:str)->str:
    with open(path,'r',encoding='utf-8') as f: return f.read()

def _cap(label:str, text:str)->str:
    m=re.search(rf"(?:^|\n)\s*(?:{label}[:\-]|{label}\.)\s*(.*)", text, flags=re.I)
    return m.group(1).strip() if m else ""

def summarize_text(text:str)->Dict:
    if DRY_RUN or get_client() is None:
        parties_line=_cap("Parties|Between", text) or text.splitlines()[0].strip()
        parties=[p.strip(", .") for p in re.split(r"\band\b|,\s*", parties_line) if p.strip()][:2]
        term=_cap("Term|Duration", text) or "Not specified"
        renewal=_cap("Renewal|Extension", text) or "Not specified"
        payment=_cap("Payment Terms|Payment", text) or "Not specified"
        bullets=re.findall(r"^[\-*]\s*(.+)$", text, flags=re.M) or [b[0].strip() for b in re.findall(r"([^\.\n]*\b(shall|must)\b[^\.\n]*\.)", text, flags=re.I)]
        obligations=bullets[:5]
        risks=[f"Check clause on {kw}" for kw in ["penalty","liability","termination","indemnify","breach","late fee","non-compete"] if re.search(kw, text, flags=re.I)]
        if not risks: risks=["No obvious risk keywords found; legal review still required."]
        return {"parties":parties,"term":term,"renewal":renewal,"payment":payment,"obligations":obligations,"risks":risks[:5]}
    client=get_client()
    messages=[{"role":"system","content":"Summarize contract to JSON fields: parties[], term, renewal, payment, obligations[], risks[]"},
              {"role":"user","content":text[:15000]}]
    schema={"type":"json_schema","json_schema":{"name":"ContractSummary","schema":{"type":"object",
            "required":["parties","term","renewal","payment","obligations","risks"],
            "properties":{"parties":{"type":"array","items":{"type":"string"}},"term":{"type":"string"},
                         "renewal":{"type":"string"},"payment":{"type":"string"},
                         "obligations":{"type":"array","items":{"type":"string"}},
                         "risks":{"type":"array","items":{"type":"string"}}}}}}
    resp=client.chat(messages,response_format=schema)
    return json.loads(resp["choices"][0]["message"]["content"])

def proc_batch(cfg:Dict)->List[Dict]:
    results=[]
    for path in cfg.get("contracts",[]):
        results.append(summarize_text(_read(path)))
    return results
