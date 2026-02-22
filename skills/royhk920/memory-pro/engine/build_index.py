from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from preprocess import preprocess_directory

def build_index():
    """
    Build FAISS index and save to specified path.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    index_dir = os.getenv("MEMORY_PRO_INDEX_DIR", base_dir)
    output_path = os.getenv("MEMORY_PRO_INDEX_PATH", os.path.join(index_dir, "memory.index"))
    sentences_path = os.path.join(index_dir, "sentences.txt")
    
    print("🔍 Starting index build...")
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    sentences = preprocess_directory()
    print(f"📊 Found {len(sentences)} valid sentences")
    embeddings = model.encode(sentences)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    
    print(f"💾 Saving index to {output_path}...")
    faiss.write_index(index, output_path)
    with open(sentences_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sentences))
    print(f"✅ Index build complete! Contains {len(sentences)} sentences")
    return sentences, index

if __name__ == "__main__":
    sentences, index = build_index()
