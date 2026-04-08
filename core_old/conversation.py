from utils.constants import STATES, EXIT_KEYWORDS
from core_old.prompts import QUESTION_GENERATION_PROMPT, FALLBACK_PROMPT, END_PROMPT
from core_old.llm import call_llm
from core_old.validators import is_valid_name, is_valid_email, is_valid_experience, is_reasonable_tech_stack

INFO_FIELDS = [
    "Full Name",
    "Email Address",
    "Job Role",
    "Years of Experience",
    "Current Location",
]

GUIDANCE = {
    "interview": "Revise core concepts, explain projects clearly, practice Python & SQL basics.",
    "skills": "Strengthen Python, build 1–2 projects, revise ML fundamentals.",
    "resume": "Improve project descriptions, add clarity, include links.",
}

def handle_conversation(user_input, session):
    state = session["state"]

    if state == STATES["GREETING"]:
        session["state"] = STATES["COLLECT_INFO"]
        session["info_index"] = 0
        return "👋 Welcome to TalentScout!\n\nWhat is your full name?"

    if user_input.lower().strip() in EXIT_KEYWORDS:
        session["state"] = STATES["END"]
        return END_PROMPT

    if state == STATES["COLLECT_INFO"]:
        field = INFO_FIELDS[session["info_index"]]

        validators = {
            "Full Name": is_valid_name,
            "Email Address": is_valid_email,
            "Job Role": lambda x: len(x) > 2,
            "Years of Experience": is_valid_experience,
            "Current Location": lambda x: len(x) > 2,
        }

        if not validators[field](user_input):
            return f"Invalid {field}. Please try again."

        session["candidate_data"][field] = user_input
        session["info_index"] += 1

        if session["info_index"] < len(INFO_FIELDS):
            return f"Please provide your {INFO_FIELDS[session['info_index']]}."

        session["state"] = STATES["COLLECT_TECH"]
        return "Please list your technical skills."

    if state == STATES["COLLECT_TECH"]:
        if not is_reasonable_tech_stack(user_input):
            return "Please list recognizable technical skills."

        session["tech_stack"] = user_input
        session["state"] = STATES["GENERATE_QUESTIONS"]

        exp = float(session["candidate_data"]["Years of Experience"])
        difficulty = "beginner" if exp < 1 else "intermediate"

        prompt = QUESTION_GENERATION_PROMPT.format(
            tech_stack=user_input,
            domain=session["candidate_data"].get("primary_domain"),
            experience=exp,
            difficulty=difficulty,
        )
        return call_llm([{"role": "user", "content": prompt}])

    if state == STATES["GENERATE_QUESTIONS"]:
        session["state"] = STATES["SUMMARY"]
        data = session["candidate_data"]
        return f"""
📄 Candidate Summary
Name: {data['Full Name']}
Email: {data['Email Address']}
Domain: {data.get('primary_domain')}
Role: {data['Job Role']}
Experience: {data['Years of Experience']}
Location: {data['Current Location']}
Tech Stack: {session['tech_stack']}

Type: interview | skills | resume | exit
"""

    if state == STATES["SUMMARY"]:
        for k in GUIDANCE:
            if k in user_input.lower():
                return GUIDANCE[k]
        return FALLBACK_PROMPT

    return FALLBACK_PROMPT
