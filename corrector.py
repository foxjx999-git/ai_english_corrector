import json

from prompts import build_correction_prompt,build_review_prompt
from openai_client import ask_ai

def correct_english(sentence):
    prompt = build_correction_prompt(sentence)

    try:
        ai_result= ask_ai(prompt)

        ai_data = json.loads(ai_result)

        result = {
            "success": True,
            "original": sentence,
            "corrected": ai_data["corrected"],
            "explanation": ai_data["explanation"],
            "natural_expression": ai_data["natural_expression"],
            "error_type": ai_data["error_type"],
            "suggestion": ai_data["suggestion"]
        }
        return result
    except Exception as e:
        result = {
            "sucess": False,
            "original": sentence,
            "error": str(e)
        }
        return result

def evaluate_review_answer(original_sentence, user_answer, reference_answer, explanation):
    prompt = build_review_prompt(
        original_sentence,
        user_answer,
        reference_answer,
        explanation
    )

    try:
        ai_result = ask_ai(prompt)
        ai_data = json.loads(ai_result)

        score = ai_data["score"]
        missing_points = ai_data["missing_points"]

        is_correct = ai_data["is_correct"]

        if missing_points or score < 95:
            is_correct = False

        result = {
            "success": True,
            "score": ai_data["score"],
            "feedback": ai_data["feedback"],
            "is_correct": is_correct,
            "missing_points": ai_data["missing_points"],
            "better_answer": ai_data["better_answer"]
        }

        return result

    except Exception as e:
        result = {
            "success": False,
            "error": str(e)
        }

        return result