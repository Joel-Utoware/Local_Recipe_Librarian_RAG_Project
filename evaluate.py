# evaluate.py

import time
from rag_pipeline import generate_answer


# ---------------------------------
# Test Queries
# ---------------------------------
test_queries = [
    "Easy spicy chicken dinner",
    "Vegetarian pasta under 30 minutes",
    "Dessert with fewer than 5 ingredients",
    "What can I cook with eggs and potatoes?",
    "Quick healthy lunch ideas"
]


# ---------------------------------
# Run Evaluation
# ---------------------------------
def run_evaluation():
    print("=" * 60)
    print("LOCAL RECIPE LIBRARIAN - QUICK EVALUATION")
    print("=" * 60)

    for i, query in enumerate(test_queries, start=1):

        print(f"\nQuery {i}: {query}")

        start_time = time.time()

        response = generate_answer(query)

        end_time = time.time()
        duration = round(end_time - start_time, 2)

        print(f"Response Time: {duration}s")
        print("Answer:")
        print(response[:500])   # first 500 chars only
        print("-" * 60)


# ---------------------------------
# Main
# ---------------------------------
if __name__ == "__main__":
    run_evaluation()