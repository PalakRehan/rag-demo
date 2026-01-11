# rag_service/indexing.py
import os
from pathlib import Path
from typing import List, Dict, Optional

# import chunker from your utils; optionally import encoding loader if present
from .utils import chunk_text_by_tokens
try:
    from .utils import load_tiktoken_encoding
except Exception:
    load_tiktoken_encoding = None  # optional helper may not exist in your utils


def extract_pdf_text(pdf_path: Path) -> str:
    """Extract text from PDF file using pdfplumber (lazy import)."""
    try:
        import pdfplumber
    except ImportError as e:
        raise ImportError("pdfplumber is required for PDF processing. Install with: pip install pdfplumber") from e

    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def index_text_file(path: str, model_name: str = "llama-3", max_tokens: int = 200, overlap: int = 50) -> List[Dict]:
    """
    Parse a single file and return token-aware chunks.
    - Does not write any index or files.
    - Returns list of chunk dicts: {"id": int, "text": str, "meta": {...}}.
    """
    safe_path = Path(path).resolve()
    if not safe_path.exists() or not safe_path.is_file():
        raise ValueError(f"Invalid or non-existent file path: {path}")

    # extract raw text
    if safe_path.suffix.lower() == ".pdf":
        text = extract_pdf_text(safe_path)
    else:
        text = safe_path.read_text(encoding="utf-8")

    # try to load encoding once if helper exists; otherwise pass None and let chunker fallback
    encoding = None
    if load_tiktoken_encoding is not None:
        try:
            encoding = load_tiktoken_encoding(model_name)
        except Exception:
            encoding = None

    # chunk the text (chunk_text_by_tokens should accept encoding or None)
    chunks = chunk_text_by_tokens(text, max_tokens=max_tokens, overlap=overlap, model_name=model_name, encoding=encoding)

    # attach source metadata
    for i, c in enumerate(chunks):
        c.setdefault("meta", {})
        c["meta"]["source"] = str(safe_path)
        # ensure unique id within this file
        c["id"] = i

    return chunks



