import os, json, requests

PINCODE=os.environ["PINCODE"]
BOT_TOKEN=os.environ["BOT_TOKEN"]
CHAT_ID=os.environ["CHAT_ID"]

PRODUCTS=json.load(open("products.json"))

STATE_FILE="state.json"
try:
    state=json.load(open(STATE_FILE))
except:
    state={}

def send(msg):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  data={"chat_id":CHAT_ID,"text":msg})

headers={"User-Agent":"Mozilla/5.0"}

for p in PRODUCTS:
    url=p["url"]
    ok=False
    try:
        r=requests.get(url,headers=headers,timeout=20)
        txt=r.text.lower()
        # Simple heuristic; adjust if Amul changes page.
        ok=("out of stock" not in txt and "sold out" not in txt)
    except:
        continue
    last=state.get(url,False)
    if ok and not last:
        send(f"✅ In stock: {p['name']}\n{url}")
    state[url]=ok

json.dump(state,open(STATE_FILE,"w"))
