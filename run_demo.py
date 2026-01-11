# scripts/inspect_chunks.py
import json
from pathlib import Path
from rag_service.indexing import index_text_file  # or index_pdf_file if you implemented pdf reader

DATA_DIR = Path("sample_data")
OUT_DIR = Path("data") 
OUT_DIR.mkdir(exist_ok=True)

all_chunks = []
for file in sorted(DATA_DIR.iterdir()):
    if file.suffix.lower() not in {".pdf", ".txt"}:
        continue
    chunks = index_text_file(str(file), model_name="llama-3", max_tokens=200, overlap=50)
    print(f"File: {file.name}  →  chunks: {len(chunks)}")
    # print first 2 chunks for quick inspection
    for c in chunks[:2]:
        print(f"  id={c['id']} tokens={c['meta']['token_start']}..{c['meta']['token_end']} text_preview={c['text'][:120]!r}")
    all_chunks.extend(chunks)

# save a small JSON for review
with open(OUT_DIR / "sample_chunks_preview.json", "w", encoding="utf-8") as f:
    json.dump(all_chunks[:50], f, ensure_ascii=False, indent=2)

print("Saved preview to data/sample_chunks_preview.json")


