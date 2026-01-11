import re
from typing import List, Dict, Optional

def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\s+", " ", text).strip()
    return text

def chunk_text_by_tokens(
    text: str,
    max_tokens: int = 200,
    overlap: int = 50,
    model_name: Optional[str] = None,
    encoding=None
) -> List[Dict]:
    text = clean_text(text)
    if not text:
        return []

    # Use cl100k_base encoding directly for all models
    try:
        if encoding is None:
            import tiktoken
            enc = tiktoken.get_encoding("cl100k_base")
        else:
            enc = encoding
        
        # Token-based chunking
        token_ids = enc.encode(text)
        step = max_tokens - overlap if (max_tokens - overlap) > 0 else max_tokens
        
        chunks: List[Dict] = []
        chunk_id = 0
        for start in range(0, len(token_ids), step):
            end = min(start + max_tokens, len(token_ids))
            chunk_ids = token_ids[start:end]
            chunk_text = enc.decode(chunk_ids)
            chunks.append({
                "id": chunk_id,
                "text": chunk_text.strip(),
                "meta": {
                    "token_start": start,
                    "token_end": end
                }
            })
            chunk_id += 1
            if end == len(token_ids):
                break
        return chunks
        
    except Exception:
        # Fallback to word-based chunking
        words = text.split()
        step = max_tokens - overlap if (max_tokens - overlap) > 0 else max_tokens
        
        chunks: List[Dict] = []
        chunk_id = 0
        for start in range(0, len(words), step):
            end = min(start + max_tokens, len(words))
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)
            chunks.append({
                "id": chunk_id,
                "text": chunk_text.strip(),
                "meta": {
                    "token_start": start,
                    "token_end": end
                }
            })
            chunk_id += 1
            if end == len(words):
                break
        return chunks