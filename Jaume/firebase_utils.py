# firebase_utils.py
import requests

PROJECT_ID = "jfleague-84a82"
BASE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"

def _unwrap(v):
    if not isinstance(v, dict):
        return v
    if "stringValue" in v:   return v["stringValue"]
    if "integerValue" in v:  return int(v["integerValue"])
    if "doubleValue" in v:   return float(v["doubleValue"])
    if "booleanValue" in v:  return v["booleanValue"]
    if "timestampValue" in v:return v["timestampValue"]
    if "arrayValue" in v:    return [_unwrap(x) for x in v["arrayValue"].get("values", [])]
    if "mapValue" in v:
        fields = v["mapValue"].get("fields", {})
        return {k: _unwrap(val) for k, val in fields.items()}
    return None

def _get_collection(name: str):
    url = f"{BASE_URL}/{name}?pageSize=200"
    r = requests.get(url)
    r.raise_for_status()
    docs = r.json().get("documents", []) or []
    out = []
    for d in docs:
        fields = d.get("fields", {}) or {}
        item = {k: _unwrap(v) for k, v in fields.items()}
        item["id"] = d["name"].split("/")[-1]
        out.append(item)
    return out

def get_players():
    return _get_collection("players")

def get_matches():
    return _get_collection("matches")

def get_match_actions():
    return _get_collection("matchActions")
