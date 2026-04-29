# retriever.py

from build_vector_db import build_database

collection = build_database()


def search_recipes(
    query_text: str,
    top_k: int = 5,
    category: str | None = None,
    subcategory: str | None = None,
    max_ingredients: int | None = None,
    max_steps: int | None = None
):
    """
    Semantic search with optional metadata filters.
    """

    if not query_text.strip():
        return []

    where_conditions = []

    # Exact category filter
    if category:
        where_conditions.append(
            {"category": {"$eq": category.lower()}}
        )

    # Exact subcategory filter
    if subcategory:
        where_conditions.append(
            {"subcategory": {"$eq": subcategory.lower()}}
        )

    # Numeric filters
    if max_ingredients is not None:
        where_conditions.append(
            {"num_ingredients": {"$lte": max_ingredients}}
        )

    if max_steps is not None:
        where_conditions.append(
            {"num_steps": {"$lte": max_steps}}
        )

    # Build final where clause
    where_clause = None

    if len(where_conditions) == 1:
        where_clause = where_conditions[0]

    elif len(where_conditions) > 1:
        where_clause = {"$and": where_conditions}

    # Query Chroma
    results = collection.query(
        query_texts=[query_text],
        n_results=top_k,
        where=where_clause
    )

    return results


if __name__ == "__main__":

    # Example:
    results = search_recipes(
        query_text="easy chicken dinner",
        top_k=3,
        category="dinner",
        max_ingredients=7,
        max_steps=5
    )

    for i in range(len(results["documents"][0])):
        print(f"\nMatch {i+1}")
        print(results["metadatas"][0][i])