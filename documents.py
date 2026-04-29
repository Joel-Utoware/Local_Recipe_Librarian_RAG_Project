# documents.py

import json
from pathlib import Path


INPUT_FILE = Path("data/processed/recipes_clean.jsonl")


def format_recipe_text(recipe: dict) -> str:
    """
    Create clean searchable text for embeddings.
    """

    ingredients = ", ".join(recipe.get("ingredients", []))
    directions = " ".join(recipe.get("directions", []))

    text = f"""
Title: {recipe.get("recipe_title", "")}

Category: {recipe.get("category", "")}
Subcategory: {recipe.get("subcategory", "")}

Description:
{recipe.get("description", "")}

Ingredients:
{ingredients}

Directions:
{directions}
""".strip()

    return text


def load_documents():
    """
    Load recipes and return:
    1. documents (text for embeddings)
    2. metadata (used later for retrieval results)
    """

    documents = []
    metadata = []

    with open(INPUT_FILE, "r", encoding="utf-8") as infile:
        for line in infile:
            recipe = json.loads(line)

            document_text = format_recipe_text(recipe)

            documents.append(document_text)

            metadata.append(
                {
                    "id": recipe.get("id"),
                    "recipe_title": recipe.get("recipe_title"),
                    "category": recipe.get("category"),
                    "subcategory": recipe.get("subcategory"),
                    "num_ingredients": recipe.get("num_ingredients"),
                    "num_steps": recipe.get("num_steps"),
                }
            )

    print(f"Loaded {len(documents)} recipe documents.")

    return documents, metadata


if __name__ == "__main__":
    docs, meta = load_documents()

    print("\nSample Document:\n")
    print(docs[0])

    print("\nSample Metadata:\n")
    print(meta[0])