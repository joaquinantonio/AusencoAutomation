import os, requests, json
DRY_RUN = os.getenv("DRY_RUN","true").lower()=="true"
XAI_API_KEY = os.getenv("XAI_API_KEY","") # xai-y8mdqBMnv6aGwqmkJ7kduYF4FGc0OmE5N2q1zdmCj4hv1Z6BiTghVbQPSpvcdznRsmidsUbBKx8YChFN
class GrokClient:
    BASE = "https://api.x.ai"
    def __init__(self, api_key): self.api_key=api_key
    def chat(self, messages, model="grok-4-fast", response_format=None, **kwargs):
        payload={"model":model,"messages":messages}
        if response_format: payload["response_format"]=response_format
        payload.update(kwargs or {})
        r=requests.post(f"{self.BASE}/v1/chat/completions",
                        headers={"Authorization":f"Bearer {self.api_key}","Content-Type":"application/json"},
                        json=payload, timeout=60)
        r.raise_for_status()
        return r.json()
def get_client():
    if not DRY_RUN and XAI_API_KEY:
        return GrokClient(XAI_API_KEY)
    return None
