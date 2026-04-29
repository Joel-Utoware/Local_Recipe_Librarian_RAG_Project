# build_vector_db.py

import chromadb
from chromadb.utils import embedding_functions
from documents import load_documents


DB_PATH = "data/processed/recipe_db"
COLLECTION_NAME = "my_recipes"
MODEL_NAME = "all-MiniLM-L6-v2"
BATCH_SIZE = 5000   # safely below Chroma max limit


def get_client():
    return chromadb.PersistentClient(path=DB_PATH)


def get_embedder():
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=MODEL_NAME
    )


def get_collection(client, embedder):
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedder
    )


def collection_has_data(collection) -> bool:
    """
    Prevent rebuilding database every UI run.
    """
    return collection.count() > 0


def add_in_batches(collection, docs, meta):
    """
    Insert documents in safe batches.
    """

    total = len(docs)

    for start in range(0, total, BATCH_SIZE):
        end = start + BATCH_SIZE

        batch_docs = docs[start:end]
        batch_meta = meta[start:end]
        batch_ids = [str(m["id"]) for m in batch_meta]

        collection.add(
            documents=batch_docs,
            metadatas=batch_meta,
            ids=batch_ids
        )

        print(f"Added {min(end, total)} / {total}")


def build_database():
    client = get_client()
    embedder = get_embedder()
    collection = get_collection(client, embedder)

    # Prevent duplicate rebuilds every run
    if collection_has_data(collection):
        print("Database already exists and contains data.")
        print(f"Stored recipes: {collection.count()}")
        return collection

    print("Loading recipe documents...")
    docs, meta = load_documents()

    print("Creating vector database...")
    add_in_batches(collection, docs, meta)

    print("Database populated and saved locally.")
    return collection


if __name__ == "__main__":
    build_database()