from utils.constants import STATES, EXIT_KEYWORDS
from core.prompts import (
    QUESTION_GENERATION_PROMPT,
    FALLBACK_PROMPT,
    END_PROMPT,
)
from core.llm import call_llm
from core.validators import (
    is_valid_name,
    is_valid_email,
    is_valid_experience,
    is_reasonable_tech_stack,
)

DOMAIN_TECH_HINTS = {
    "AI / Machine Learning": "Python, NumPy, Pandas, Scikit-learn, PyTorch, TensorFlow, LangChain, RAG",
    "Backend Engineering": "Python, Java, Node.js, Django, FastAPI, SQL",
    "Frontend Engineering": "JavaScript, React, HTML, CSS",
    "Data Science / Analytics": "Python, SQL, Pandas, Statistics",
    "DevOps / Cloud": "AWS, Docker, Kubernetes, CI/CD",
}

GUIDANCE_INTENTS = {
    "interview": ["interview", "prepare", "prep", "guide"],
    "skills": ["skill", "learn", "train", "improve"],
    "resume": ["resume", "cv"],
}

INFO_FIELDS = [
    "Full Name",
    "Email Address",
    "Job Role",
    "Years of Experience",
    "Current Location",
]


def user_wants_exit(text: str) -> bool:
    return text.lower().strip() in EXIT_KEYWORDS


def detect_guidance_intent(text: str):
    t = text.lower()
    for intent, keywords in GUIDANCE_INTENTS.items():
        if any(k in t for k in keywords):
            return intent
    return None


def handle_conversation(user_input: str, session: dict) -> str:
    state = session["state"]

    # ---------- GREETING ----------
    if state == STATES["GREETING"]:
        session["state"] = STATES["COLLECT_INFO"]
        session["info_index"] = 0
        return (
            "👋 **Welcome to TalentScout!**\n\n"
            "I’ll guide you through a short recruitment screening.\n\n"
            "**What is your full name?**"
        )

    # ---------- EXIT ----------
    if user_wants_exit(user_input):
        session["state"] = STATES["END"]
        return END_PROMPT

    # ---------- INFO COLLECTION ----------
    if state == STATES["COLLECT_INFO"]:
        idx = session["info_index"]
        field = INFO_FIELDS[idx]

        validators = {
            "Full Name": is_valid_name,
            "Email Address": is_valid_email,
            "Job Role": lambda x: len(x.strip()) >= 3,
            "Years of Experience": is_valid_experience,
            "Current Location": lambda x: len(x.strip()) >= 2,
        }

        if not validators[field](user_input):
            if field == "Email Address":
                return (
                    "That doesn’t look like a valid email.\n\n"
                    "Example: `name@example.com`\n\n"
                    "Please try again."
                )
            return f"That doesn’t look like a valid **{field}**. Please try again."

        session["candidate_data"][field] = user_input
        session["info_index"] += 1

        if session["info_index"] < len(INFO_FIELDS):
            return f"Please provide your **{INFO_FIELDS[session['info_index']]}**."

        session["state"] = STATES["COLLECT_TECH"]
        return (
            "📌 **Technical Assessment Guidelines**\n\n"
            "- Initial screening only\n"
            "- Focus on explaining your thinking\n"
            "- No right or wrong answers\n\n"
            "Please list your **technical skills**."
        )

    # ---------- TECH STACK ----------
    if state == STATES["COLLECT_TECH"]:
        domain = session["candidate_data"].get("primary_domain", "")

        if not is_reasonable_tech_stack(user_input):
            return (
                f"For **{domain}**, typical tools include:\n\n"
                f"{DOMAIN_TECH_HINTS.get(domain)}\n\n"
                "Please list your technical skills."
            )

        session["tech_stack"] = user_input
        session["state"] = STATES["GENERATE_QUESTIONS"]

        experience = float(session["candidate_data"]["Years of Experience"])
        difficulty = (
            "beginner-level"
            if experience < 1
            else "intermediate-level"
            if experience < 3
            else "advanced-level"
        )

        prompt = QUESTION_GENERATION_PROMPT.format(
            tech_stack=user_input,
            domain=domain,
            experience=experience,
            difficulty=difficulty,
        )

        return call_llm([{"role": "user", "content": prompt}])

    # ---------- SUMMARY + GUIDANCE ----------
    if state == STATES["GENERATE_QUESTIONS"]:
        session["state"] = STATES["SUMMARY"]
        data = session["candidate_data"]

        return f"""
### 📄 Candidate Summary

- **Name:** {data.get("Full Name")}
- **Email:** {data.get("Email Address")}
- **Domain:** {data.get("primary_domain")}
- **Job Role:** {data.get("Job Role")}
- **Experience:** {data.get("Years of Experience")} years
- **Location:** {data.get("Current Location")}
- **Tech Stack:** {session.get("tech_stack")}

---

### 👉 What would you like to do next?
Type:
- **Interview preparation**
- **Skill improvement**
- **Resume advice**
- **Exit**
"""

    if state == STATES["SUMMARY"]:
        intent = detect_guidance_intent(user_input)

        if intent == "interview":
            return (
                "🎯 **Interview Preparation Tips**\n\n"
                "- Revise core concepts\n"
                "- Practice explaining projects\n"
                "- Prepare basic SQL & Python questions\n\n"
                "You can also ask for **skills** or **resume advice**."
            )

        if intent == "skills":
            return (
                "📚 **Skill Improvement Roadmap (4–6 weeks)**\n\n"
                "- Strengthen Python & Pandas\n"
                "- Build 1–2 real projects\n"
                "- Practice ML basics\n\n"
                "You can also ask for **interview** or **resume advice**."
            )

        if intent == "resume":
            return (
                "📄 **Resume Improvement Advice**\n\n"
                "- Add measurable achievements\n"
                "- Clearly list tools & skills\n"
                "- Include project links\n\n"
                "You can also ask for **interview** or **skills guidance**."
            )

        return FALLBACK_PROMPT

    return FALLBACK_PROMPT
