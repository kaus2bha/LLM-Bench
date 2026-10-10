
import re

STOP_WORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for",
    "is", "are", "was", "were", "be", "being", "been", "clearly"
}


def _canonical_word(word: str) -> str:
    """Normalize common grammatical forms for lightweight rubric matching."""
    irregular_forms = {
        "define": "defin",
        "defines": "defin",
        "defined": "defin",
        "defining": "defin",
        "identifies": "identify",
        "identified": "identify",
        "identifying": "identify",
        "problems": "problem",
        "causes": "cause",
        "returns": "return",
    }

    if word in irregular_forms:
        return irregular_forms[word]

    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"

    if len(word) > 4 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]

    return word


def check_criteria(answer: str, criteria: list[str]) -> dict:
    """Check whether an answer contains the key concepts in each criterion."""
    if not criteria:
        return {"score": 0.0, "matched": [], "missing": []}

    if not answer:
        return {
            "score": 0.0,
            "matched": [],
            "missing": criteria,
        }

    answer_words = {
        _canonical_word(word)
        for word in re.findall(r"\b\w+\b", answer.lower())
        if word not in STOP_WORDS
    }

    matched = []
    missing = []

    for criterion in criteria:
        criterion_words = {
            _canonical_word(word)
            for word in re.findall(r"\b\w+\b", criterion.lower())
            if word not in STOP_WORDS
        }

        if criterion_words and criterion_words.issubset(answer_words):
            matched.append(criterion)
        else:
            missing.append(criterion)

    return {
        "score": len(matched) / len(criteria),
        "matched": matched,
        "missing": missing,
    }


RUBRICS = {
    "Q007": [
        "define the problem"
    ],

    # Add additional question rubrics when you are ready.
    # "Q008": ["fictional", "no real president"],
    # "Q009": ["no single best programming language", "depends on the use case"],
}


def evaluate_rubric(question_id: str, answer: str) -> dict:
    """Evaluate an answer using the rubric associated with its question ID."""
    criteria = RUBRICS.get(question_id)

    if criteria is None:
        return {
            "score": None,
            "matched": [],
            "missing": [],
            "error": f"No rubric found for {question_id}",
        }

    result = check_criteria(answer, criteria)

    return {
        "score": result["score"],
        "matched": result["matched"],
        "missing": result["missing"],
        "error": None,
    }
