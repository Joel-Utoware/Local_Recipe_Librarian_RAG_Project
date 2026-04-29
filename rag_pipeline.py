# rag_pipeline.py

import ollama
from retriever import search_recipes


MODEL_NAME = "phi3"   # Excellent for 8GB RAM laptops


def generate_answer(query: str) -> str:
    """
    Retrieve recipe context and generate grounded answer.
    """

    # Search vector database
    results = search_recipes(query, top_k=3)

    # Handle no results
    if not results or not results["documents"][0]:
        return "I couldn't find any relevant recipes."

    # Build context from retrieved recipes
    retrieved_docs = results["documents"][0]
    context = "\n\n---\n\n".join(retrieved_docs)

    # Strong RAG system prompt
    system_prompt = """
You are a helpful recipe assistant.

Use ONLY the recipe context provided.

Rules:
1. If the answer is not in the context, say you don't know.
2. Keep answers practical and concise.
3. If multiple recipes fit, summarize the best options.
4. When relevant, mention ingredients and steps clearly.
""".strip()

    # User prompt
    user_message = f"""
Recipe Context:
{context}

Question:
{query}
""".strip()

    # Local model call
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        options={
            "temperature": 0.2,
            "num_predict": 300
        }
    )

    return response["message"]["content"]


if __name__ == "__main__":
    my_query = "How do I make a spicy chicken dish?"

    answer = generate_answer(my_query)

    print("\n--- Recipe Assistant Response ---\n")
    print(answer)