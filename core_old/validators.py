import re

def is_valid_name(name: str) -> bool:
    return len(name.strip()) >= 2 and any(c.isalpha() for c in name)

def is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))

def is_valid_experience(exp: str) -> bool:
    try:
        val = float(exp)
        return 0 <= val <= 50
    except ValueError:
        return False

def is_reasonable_tech_stack(stack: str) -> bool:
    keywords = [
        "python", "java", "javascript", "sql", "aws", "docker",
        "react", "django", "flask", "fastapi", "node",
        "tensorflow", "pytorch", "kubernetes", "langchain", "rag"
    ]
    s = stack.lower()
    return any(k in s for k in keywords)
