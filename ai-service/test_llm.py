import time
from app.services.llm import generate_question, evaluate_answer

# --- Test Question Generation ---
print("--- Question 1 ---")
print(generate_question("DSA", "medium"))
time.sleep(2)  # Give the rate limiter a quick moment to breathe

print("\n--- Question 2 ---")
print(generate_question("HR", "easy"))
time.sleep(2)

print("\n--- Question 3 ---")
print(generate_question("System Design", "hard"))
time.sleep(2)


# --- Test Answer Evaluation ---
print("\n--- Evaluation Test ---")
result = evaluate_answer(
    question="What is the time complexity of binary search?",
    answer="It's O(log n) because we halve the search space each time.",
    interview_type="DSA"
)

print("Result Dictionary:")
print(result)

print("\nData Type:")
print(type(result))