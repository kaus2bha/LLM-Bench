
import re
import unicodedata


def exact_match(predicted: str, ground_truth: str) -> bool:
    """Check whether two answers match exactly after trimming whitespace."""
    if predicted is None or ground_truth is None:
        return False

    return predicted.strip() == ground_truth.strip()


def normalize_text(text: str) -> str:
    """
    Normalize text for answer comparison.

    Handles case, punctuation, whitespace, common unit variants,
    and common Unicode representations of squared units.
    """
    if text is None:
        return ""

    text = unicodedata.normalize("NFKC", str(text)).lower().strip()

    # Normalize common area-unit variants.
    text = re.sub(
        r"\b(square\s+centimeters?|sq\.?\s*cm|cm\s*2)\b",
        "square centimeter",
        text,
    )
    text = re.sub(r"\bcm²\b", "square centimeter", text)
    text = re.sub(r"\bsquare\s+centimetres?\b", "square centimeter", text)

    # Normalize common time-unit variants.
    text = re.sub(r"\bdays?\b", "day", text)

    # Remove punctuation and normalize whitespace.
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def _contains_answer(predicted: str, ground_truth: str) -> bool:
    """Check for a whole-word answer phrase inside a longer response."""
    if not ground_truth:
        return False

    # Do not accept a target phrase when it is explicitly negated.
    pattern = rf"(?<!\w){re.escape(ground_truth)}(?!\w)"

    for match in re.finditer(pattern, predicted):
        preceding_text = predicted[max(0, match.start() - 20):match.start()]

        if re.search(r"\b(not|never|isn't|aren't|wasn't|weren't|cannot|can't)\s*$",
                     preceding_text):
            continue

        return True

    return False


def normalized_match(predicted: str, ground_truth: str) -> bool:
    """
    Compare answers after normalization.

    Supports:
    - Exact normalized matches
    - Correct answers embedded in explanatory sentences
    - Numeric answers provided without their expected unit
    """
    if predicted is None or ground_truth is None:
        return False

    predicted_normalized = normalize_text(predicted)
    truth_normalized = normalize_text(ground_truth)

    if not predicted_normalized or not truth_normalized:
        return False

    if predicted_normalized == truth_normalized:
        return True

    # Accept a ground-truth phrase embedded in a longer explanation.
    if _contains_answer(predicted_normalized, truth_normalized):
        return True

    # Permit a bare numeric answer when the ground truth includes a unit,
    # such as "6" versus "6 days". Require the prediction to be only a number.
    if re.fullmatch(r"[-+]?\d+(?:\.\d+)?", predicted_normalized):
        truth_numbers = re.findall(r"[-+]?\d+(?:\.\d+)?", truth_normalized)

        if truth_numbers and predicted_normalized == truth_numbers[0]:
            return True

    return False
