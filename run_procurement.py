import os, json, csv
from app.services.procurement import proc_batch
def main():
    cfg_path=os.getenv("PROC_CONFIG","config/proc.json")
    with open(cfg_path,'r',encoding='utf-8') as f: cfg=json.load(f)
    res=proc_batch(cfg)
    reg=cfg.get("outputs",{}).get("register_path","out/contracts_register.csv")
    os.makedirs(os.path.dirname(reg),exist_ok=True)
    with open(reg,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(["parties","term","renewal","payment","obligations","risks"])
        for r in res:
            w.writerow([" & ".join(r.get("parties",[])), r.get("term",""), r.get("renewal",""),
                        r.get("payment",""), " | ".join(r.get("obligations",[])), " | ".join(r.get("risks",[]))])
    print(f"Wrote {reg}")
if __name__=='__main__': main()
