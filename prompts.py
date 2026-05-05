def build_correction_prompt(sentence):
    prompt = f"""
You are an English correction assistant.

Please correct the user's English sentence.

Use Simplified Chinese for explanation and suggestion.

User sentence:
{sentence}

Please return only valid JSON. Do not use markdown.

The JSON format must be:

{{
  "corrected": "the corrected sentence",
  "explanation": "explain the problems in Chinese",
  "natural_expression": "a more natural English expression"
  "error_type": ["choose one or more from: capitalization, grammar, word_choice, subject_verb_agreement, punctuation, chinese_english, other"],
  "suggestion": "give the learner a short study suggestion in Chinese"
}}
"""
    return prompt

def build_review_prompt(original_sentence, user_answer, reference_answer, explanation):
    prompt = f"""
You are an English learning coach for a Chinese learner.

The learner is reviewing a previous mistake.

Original sentence:
{original_sentence}

Learner's revised sentence:
{user_answer}

Reference answer:
{reference_answer}

Original explanation:
{explanation}

Please evaluate the learner's revised sentence.

Use Simplified Chinese.

Set is_correct to true only when the learner's sentence is fully correct, including capitalization and punctuation.

The score must be an integer from 0 to 100.

If the learner's answer is not fully correct, missing_points must include at least one specific remaining problem.

Please return only valid JSON. Do not use markdown.

The JSON format must be:

{{
  "score": 0,
  "feedback": "evaluate the learner's answer in Simplified Chinese",
  "is_correct": false,
  "missing_points": ["list the remaining problems in Simplified Chinese"],
  "better_answer": "write the best corrected sentence"
}}
"""
    return prompt