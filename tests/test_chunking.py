import tempfile
from rag_service.indexing import index_text_file

def test_chunking_small():
    txt = "word " * 450  # 450 words
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".txt") as f:
        f.write(txt)
        path = f.name
    chunks = index_text_file(path, max_tokens=200)
    assert len(chunks) >= 1
    assert all("text" in c and "meta" in c for c in chunks)