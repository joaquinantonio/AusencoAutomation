import re, json
from typing import Dict, List
from app.llm.client import get_client, DRY_RUN

def _extract(policy:str, question:str, k:int=3)->List[str]:
    lines=[ln.strip() for ln in policy.splitlines() if ln.strip()]
    q=set(re.findall(r"[A-Za-z]{3,}", question.lower()))
    scored=[]
    for ln in lines:
        t=set(re.findall(r"[A-Za-z]{3,}", ln.lower()))
        s=len(q & t)
        if s>0: scored.append((s,ln))
    scored.sort(reverse=True, key=lambda x:x[0])
    return [ln for _,ln in scored[:k]]

def answer(policy_text:str, question:str)->Dict:
    cits=_extract(policy_text, question, 3)
    if DRY_RUN or get_client() is None:
        if not cits: return {"answer":"Not in policy.","citations":[]}
        return {"answer":" ".join(cits[:2]), "citations":cits}
    client=get_client()
    messages=[{"role":"system","content":"Answer ONLY from given excerpts, else 'Not in policy.' Return JSON {answer,citations[]}."},
              {"role":"user","content":f"Excerpts:\n{chr(10).join(cits)}\n\nQuestion: {question}"}]
    schema={"type":"json_schema","json_schema":{"name":"HRAnswer","schema":{"type":"object","required":["answer","citations"],
            "properties":{"answer":{"type":"string"},"citations":{"type":"array","items":{"type":"string"}}}}}}
    resp=client.chat(messages,response_format=schema)
    return json.loads(resp["choices"][0]["message"]["content"])

def hr_batch(cfg:Dict)->List[Dict]:
    with open(cfg["policy_path"],"r",encoding="utf-8") as f: policy=f.read()
    return [answer(policy, q) for q in cfg.get("questions",[])]
