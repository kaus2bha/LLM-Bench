import re


def extract_final_answer(response: str) -> str:
    """
    Extract the final answer from an LLM response.

    Removes <think>...</think> blocks.
    If a <think> block is not closed, everything from
    <think> onward is removed.
    """
    if not response:
        return ""

    # Remove complete thinking blocks
    cleaned = re.sub(
        r"<think>.*?</think>",
        "",
        response,
        flags=re.DOTALL | re.IGNORECASE
    )

    # Handle an unclosed <think> block caused by
    # truncated model output
    cleaned = re.sub(
        r"<think>.*$",
        "",
        cleaned,
        flags=re.DOTALL | re.IGNORECASE
    )

    return cleaned.strip()