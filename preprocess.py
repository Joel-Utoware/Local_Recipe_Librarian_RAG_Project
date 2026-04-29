import os
import re
import json
from pathlib import Path
from typing import List, Optional

import pandas as pd

# Paths / constants
RAW_CSV = "data/raw/Recipes.csv"
PROCESSED_DIR = "data/processed"
RAW_JSONL = f"{PROCESSED_DIR}/recipes.jsonl"
CLEAN_JSONL = f"{PROCESSED_DIR}/recipes_clean.jsonl"


def csv_to_jsonl(input_csv: str = RAW_CSV, output_file: str = RAW_JSONL) -> int:
    """
    Convert CSV rows to JSONL. Returns number of rows written.
    """
    Path(PROCESSED_DIR).mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(input_csv)
    with open(output_file, "w", encoding="utf-8") as f:
        for idx, row in df.iterrows():
            recipe = {
                "id": int(idx) + 1,
                "recipe_title": row.get("recipe_title"),
                "category": row.get("category"),
                "subcategory": row.get("subcategory"),
                "description": row.get("description"),
                "ingredients": row.get("ingredients"),
                "directions": row.get("directions"),
                "num_ingredients": row.get("num_ingredients"),
                "num_steps": row.get("num_steps"),
            }
            f.write(json.dumps(recipe, ensure_ascii=False) + "\n")
    return len(df)


# ----------------------------
# Cleaning helpers
# ----------------------------
def clean_text(value: Optional[str]) -> str:
    if value is None:
        return ""
    value = str(value).strip()
    value = re.sub(r"\s+", " ", value)
    return value


def normalize_title(text: Optional[str]) -> str:
    return clean_text(text).title()


def normalize_category(text: Optional[str]) -> str:
    return clean_text(text).lower()


def parse_number(value) -> int:
    try:
        return int(float(value))
    except Exception:
        return 0


def normalize_ingredients(text: Optional[str]) -> List[str]:
    text = clean_text(text)
    if not text:
        return []
    parts = re.split(r"[|,;]+", text)
    cleaned = []
    for item in parts:
        item = clean_text(item).lower()
        if item:
            cleaned.append(item)
    # dedupe while preserving order
    seen = set()
    result = []
    for item in cleaned:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def normalize_directions(text: Optional[str]) -> List[str]:
    text = clean_text(text)
    if not text:
        return []
    # split on numbered steps (1. or 1) ) or on sentence breaks
    steps = re.split(r"\s*\d+\)\s*|\s*\d+\.\s*|(?<=\.)\s+", text)
    cleaned_steps = [clean_text(s) for s in steps if clean_text(s)]
    return cleaned_steps


def build_search_text(recipe: dict) -> str:
    return (
        f"Title: {recipe.get('recipe_title','')}\n"
        f"Category: {recipe.get('category','')}\n"
        f"Subcategory: {recipe.get('subcategory','')}\n"
        f"Description: {recipe.get('description','')}\n"
        f"Ingredients: {', '.join(recipe.get('ingredients',[]))}\n"
        f"Directions: {' '.join(recipe.get('directions',[]))}"
    ).strip()


# ----------------------------
# Main Cleaning Pipeline
# ----------------------------
def clean_jsonl(input_file: str = RAW_JSONL, output_file: str = CLEAN_JSONL) -> None:
    seen_titles = set()
    cleaned_count = 0
    skipped_count = 0

    Path(PROCESSED_DIR).mkdir(parents=True, exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as infile, \
         open(output_file, "w", encoding="utf-8") as outfile:

        for line in infile:
            raw = json.loads(line)

            recipe = {
                "id": raw.get("id"),
                "recipe_title": normalize_title(raw.get("recipe_title")),
                "category": normalize_category(raw.get("category")),
                "subcategory": normalize_category(raw.get("subcategory")),
                "description": clean_text(raw.get("description")),
                "ingredients": normalize_ingredients(raw.get("ingredients")),
                "directions": normalize_directions(raw.get("directions")),
                "num_ingredients": parse_number(raw.get("num_ingredients")),
                "num_steps": parse_number(raw.get("num_steps")),
            }

            if not recipe["recipe_title"]:
                skipped_count += 1
                continue

            key = recipe["recipe_title"].lower()
            if key in seen_titles:
                skipped_count += 1
                continue
            seen_titles.add(key)

            recipe["num_ingredients"] = len(recipe["ingredients"])
            recipe["num_steps"] = len(recipe["directions"])
            recipe["document_text"] = build_search_text(recipe)

            outfile.write(json.dumps(recipe, ensure_ascii=False) + "\n")
            cleaned_count += 1

    print(f"Finished cleaning. Saved: {cleaned_count} recipes. \nSkipped: {skipped_count}. \nOutput: {output_file}")


def main(run_csv_conversion: bool = True):
    if run_csv_conversion:
        n = csv_to_jsonl()
        print(f"Saved {n} recipes to {RAW_JSONL}")
    clean_jsonl()


if __name__ == "__main__":
    main()