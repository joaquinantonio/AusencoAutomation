import os, json, csv
from app.services.finance import draft_finance_report
def main():
    cfg_path=os.getenv("FINANCE_CONFIG","config/finance.json")
    with open(cfg_path,'r',encoding='utf-8') as f: cfg=json.load(f)
    res=draft_finance_report(cfg)
    outj=cfg.get("outputs",{}).get("json_path","out/finance_report.json")
    os.makedirs(os.path.dirname(outj),exist_ok=True)
    with open(outj,'w',encoding='utf-8') as f: json.dump(res,f,indent=2)
    outc=cfg.get("outputs",{}).get("csv_append_path","out/finance_variances.csv")
    with open(outc,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=["account","actual","budget","variance_pct"]); w.writeheader()
        for r in res.get("variance_table",[]): w.writerow(r)
    print(f"Wrote {outj} and {outc}")
if __name__=='__main__': main()
