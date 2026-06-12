import json
import time
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from app.config import settings

genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

VALID_TYPES = {"DSA", "CS Fundamentals", "HR", "System Design"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}

def generate_question(interview_type: str, difficulty: str = "medium") -> str:
    if interview_type not in VALID_TYPES:
        raise ValueError(f"Invalid interview type: {interview_type}")
    if difficulty not in VALID_DIFFICULTIES:
        raise ValueError(f"Invalid difficulty: {difficulty}")

    prompt = f"""You are an interview question generator for a technical interview prep app.

Generate exactly ONE {difficulty}-level interview question for the category: {interview_type}.

Rules:
- Output ONLY the question text.
- No preamble like "Here's a question:".
- No numbering, no markdown formatting.
- No answer or explanation — question only.
"""
    
    while True:
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except ResourceExhausted:
            print("\n[Rate Limit] Requests-per-minute hit. Sleeping for 30s...")
            time.sleep(30)

def evaluate_answer(question: str, answer: str, interview_type: str) -> dict:
    prompt = f"""You are an expert interviewer evaluating a candidate's answer.

Interview category: {interview_type}
Question: {question}
Candidate's answer: {answer}

Evaluate the answer and respond ONLY with valid JSON in this exact format:
{{
  "score": <integer 0-10>,
  "feedback": "<2-3 sentence feedback on the answer>",
  "missed_points": ["<key point 1 missed>", "<key point 2 missed>"]
}}

If the answer is correct/complete, missed_points can be an empty array.
Do not include any text outside the JSON object.
"""

    while True:
        try:
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            raw_text = response.text.strip()
            break  # Break out of loop if request succeeded
        except ResourceExhausted:
            print("\n[Rate Limit] Evaluation blocked. Sleeping for 30s before retry...")
            time.sleep(30)

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return {
            "score": 0,
            "feedback": "Failed to parse system evaluation.",
            "missed_points": ["Could not evaluate response."]
        }