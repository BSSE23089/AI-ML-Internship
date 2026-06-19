from chunking import load_chunks
from embeddings import get_embedding
from vector_store import add_chunk

chunks = load_chunks("netsol_faq.csv")

for i, chunk in enumerate(chunks):
    print(f"Embedding chunk {i+1}/{len(chunks)}")
    embedding = get_embedding(chunk["text"])
    add_chunk(
        chunk_id=f"faq_{i}",
        embedding=embedding,
        chunk_text=chunk["text"],
        metadata={"question": chunk["question"], "answer": chunk["answer"]}
    )

print("Done. All chunks embedded and stored.")