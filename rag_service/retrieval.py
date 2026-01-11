from typing import List, Dict

# Placeholder embedding function
def embed_text(text: str):
    # deterministic simple embedding for tests: length and hash
    return [len(text), hash(text) % 1000]

def simple_search(index: List[Dict], query: str, top_k: int = 3) -> List[Dict]:
    q_emb = embed_text(query)
    # naive distance by absolute difference of lengths
    scored = []
    for item in index:
        emb = embed_text(item["text"])
        score = abs(q_emb[0] - emb[0])
        scored.append((score, item))
    scored.sort(key=lambda x: x[0])
    return [it for _, it in scored[:top_k]]

