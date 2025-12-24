from utils.constants import EXIT_KEYWORDS


def normalize_text(text: str) -> str:
    """
    Normalize user input for safe processing.
    """
    if not text:
        return ""
    return text.strip()


def is_exit_intent(text: str) -> bool:
    """
    Check if user wants to end the conversation.
    """
    return normalize_text(text).lower() in EXIT_KEYWORDS


def clean_tech_stack(text: str) -> str:
    """
    Normalize tech stack input into a readable string.
    """
    text = normalize_text(text)
    return text.replace("\n", ", ").replace("  ", " ")


def parse_experience(text: str) -> float | None:
    """
    Extract numeric years of experience from input.
    Returns None if parsing fails.
    """
    try:
        return float(text)
    except ValueError:
        return None
