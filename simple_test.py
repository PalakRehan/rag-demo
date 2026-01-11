from rag_service import hello_world
from rag_service.utils import chunk_text_by_tokens

print(hello_world())

# Test chunking with fallback
test_text = "This is a test text with multiple words to check chunking functionality."
chunks = chunk_text_by_tokens(test_text, max_tokens=5, overlap=1)

print(f"Created {len(chunks)} chunks:")
for chunk in chunks:
    print(f"  Chunk {chunk['id']}: {chunk['text'][:50]}...")