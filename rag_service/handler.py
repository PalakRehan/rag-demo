from typing import List, Dict
from .indexing import chunk_pdf_text
from .storage import save_index, load_index
from .retrieval import simple_search

INDEX_PATH = "data/index.json"

def ensure_index(pdf_path: str):
    if not os.path.exists(INDEX_PATH):
        chunks = chunk_pdf_text(pdf_path)
        save_index(chunks, INDEX_PATH)
    return load_index(INDEX_PATH)

def query_index(query: str, top_k: int = 3) -> List[Dict]:
    index = load_index(INDEX_PATH)
    return simple_search(index, query, top_k)

