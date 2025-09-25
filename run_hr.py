import os, json, csv
from app.services.hr import hr_batch
def main():
    cfg_path=os.getenv("HR_CONFIG","config/hr.json")
    with open(cfg_path,'r',encoding='utf-8') as f: cfg=json.load(f)
    ans=hr_batch(cfg)
    outp=cfg.get("outputs",{}).get("log_path","out/hr_qna_log.csv")
    os.makedirs(os.path.dirname(outp),exist_ok=True)
    with open(outp,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(["question","answer","citations"])
        for q,a in zip(cfg.get("questions",[]), ans):
            w.writerow([q, a.get("answer",""), " | ".join(a.get("citations",[]))])
    print(f"Wrote {outp}")
if __name__=='__main__': main()
