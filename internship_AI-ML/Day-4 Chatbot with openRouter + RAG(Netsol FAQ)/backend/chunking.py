import pandas as pd


def load_chunks(csv_path: str):
    df = pd.read_csv(csv_path)
    chunks = []
    for _, row in df.iterrows():
        chunk_text = f"Q: {row['question']} A: {row['answer']}"
        chunks.append({
            "text": chunk_text,
            "question": row["question"],
            "answer": row["answer"]
        })
    return chunks