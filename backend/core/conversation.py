from utils.constants import STATES, EXIT_KEYWORDS
from backend.core.prompts import FALLBACK_PROMPT, END_PROMPT
from backend.core.llm import call_llm
from backend.core.validators import is_valid_name, is_valid_email, is_valid_experience

CUSTOM_STATES = {
    "MODE_SELECTION": "mode_selection",
    "VERIFY_INFO": "verify_info",
    "SKILL_ANALYSIS": "skill_analysis",
    "PROJECT_DEEP_DIVE": "project_deep_dive",
    "INTERVIEW": "interview",
    "FINAL_DECISION": "final_decision",
}

# ---------------------------
# HELPERS
# ---------------------------

def analyze_skills(role, skills, exp):
    prompt = f"""
You are a realistic technical recruiter.

Candidate Role: {role}
Experience: {exp} years
Skills: {skills}

IMPORTANT:
- Consider project-based strength even if fresher

Return:
1. Skill Level
2. Strengths
3. Missing Skills
4. Domain Match Score (0-10)
"""
    return call_llm([{"role": "user", "content": prompt}])


def generate_project_question(projects):
    prompt = f"""
You are a senior interviewer.

Candidate Projects:
{projects}

Ask ONE deep question covering:
- problem solved
- architecture
- deployment
- tradeoffs

Return only question.
"""
    return call_llm([{"role": "user", "content": prompt}])


def generate_question(session):
    prompt = f"""
Role: {session["candidate_data"].get("Job Role")}
Tech: {session.get("tech_stack")}

Generate ONE practical question.
"""
    return call_llm([{"role": "user", "content": prompt}])


def evaluate_answer(q, ans):
    prompt = f"""
Evaluate:

Q: {q}
A: {ans}

Return:

Score: X/10
Strengths:
- ...
Gaps:
- ...
Follow-up Question:
- ...
"""
    return call_llm([{"role": "user", "content": prompt}])

def generate_summary(session):
    scores = []

    for e in session.get("evaluation", []):
        if "Score:" in e:
            try:
                val = int(e.split("Score:")[1].split("/")[0].strip())
                scores.append(val)
            except:
                pass

    # ✅ HANDLE NO EVALUATION CASE
    if not scores:
        return f"""
📊 Candidate Summary:

⚠️ Interview not completed — no evaluation data available.

Suggestion:
- Complete the interview to receive a detailed performance assessment.

Overall Recommendation:
- Incomplete Evaluation
"""

    avg = sum(scores)/len(scores)

    return f"""
📊 Candidate Summary:

Average Score: {round(avg,1)}/10

Strength Area:
- Strong in applied problem solving and practical implementation

Improvement Area:
- Needs deeper explanations and system-level clarity

Overall Recommendation:
- {'Strong Hire' if avg >= 7 else 'Consider' if avg >=5 else 'Needs Improvement'}
"""

def final_decision(session):
    prompt = f"""
Candidate:
{session["candidate_data"]}

Evaluations:
{session["evaluation"]}

Return:

Overall Score: X/100
Strengths:
- ...
Weaknesses:
- ...
Final Decision:
- Reject / Consider / Strong Hire
"""
    return call_llm([{"role": "user", "content": prompt}])


# ---------------------------
# MAIN ENGINE
# ---------------------------

def handle_conversation(user_input, session):

    if "initialized" not in session:
        session.update({
            "initialized": True,
            "mode": session.get("mode"),
            "candidate_data": session.get("candidate_data", {}),
            "tech_stack": session.get("tech_stack", ""),
            "projects": session.get("projects", []),
            "questions": [],
            "evaluation": [],
            "current_q": 0,
            "project_done": False
        })
        session["state"] = CUSTOM_STATES["MODE_SELECTION"]

    state = session["state"]

    if user_input.lower().strip() in EXIT_KEYWORDS:
        summary = generate_summary(session)
        session["state"] = STATES["END"]
        return f"""
{summary}

Thank you for completing the screening process. Our recruitment team will review your profile and contact you if shortlisted.
"""

    # ---------------------------
    # AUTO RESUME FLOW
    # ---------------------------
    if state == CUSTOM_STATES["MODE_SELECTION"]:

        if session.get("mode") == "resume":
            session["state"] = CUSTOM_STATES["VERIFY_INFO"]

            data = session["candidate_data"]

            return f"""
📄 Resume detected:

Name: {data.get("Full Name")}
Role: {data.get("Job Role")}
Skills: {session.get("tech_stack")}

👉 Confirm? (yes/edit)
"""

        return "Type 'manual' to start."

    # ---------------------------
    # MODE HANDLING
    # ---------------------------
    if not session.get("mode"):

        if "manual" in user_input.lower():
            session["mode"] = "manual"
            session["state"] = STATES["COLLECT_INFO"]
            session["info_index"] = 0
            return "Enter your Full Name"

        return "Type 'manual' to continue."

    # ---------------------------
    # VERIFY
    # ---------------------------
    if state == CUSTOM_STATES["VERIFY_INFO"]:

        if "yes" in user_input.lower():
            session["state"] = CUSTOM_STATES["SKILL_ANALYSIS"]
            return "Analyzing your profile..."

        if "edit" in user_input.lower():
            session["mode"] = "manual"
            session["state"] = STATES["COLLECT_INFO"]
            session["info_index"] = 0
            return "Enter your Full Name"

        return "Reply yes or edit"

    # ---------------------------
    # MANUAL FLOW
    # ---------------------------
    if session["mode"] == "manual":

        fields = ["Full Name","Email Address","Job Role","Years of Experience","Location"]

        if state == STATES["COLLECT_INFO"]:

            field = fields[session["info_index"]]

            validators = {
                "Full Name": is_valid_name,
                "Email Address": is_valid_email,
                "Job Role": lambda x: True,
                "Years of Experience": is_valid_experience,
                "Location": lambda x: True,
            }

            if not validators[field](user_input):
                return f"Invalid {field}"

            session["candidate_data"][field] = user_input
            session["info_index"] += 1

            if session["info_index"] < len(fields):
                return f"Enter {fields[session['info_index']]}"

            session["state"] = STATES["COLLECT_TECH"]
            return "Enter your skills"

        if state == STATES["COLLECT_TECH"]:
            session["tech_stack"] = user_input
            session["state"] = CUSTOM_STATES["SKILL_ANALYSIS"]
            return "Processing skills..."

    # ---------------------------
    # SKILL ANALYSIS
    # ---------------------------
    if state == CUSTOM_STATES["SKILL_ANALYSIS"]:

        analysis = analyze_skills(
            session["candidate_data"].get("Job Role"),
            session.get("tech_stack"),
            session["candidate_data"].get("Years of Experience")
        )

        session["state"] = CUSTOM_STATES["PROJECT_DEEP_DIVE"]

        return f"""
🔍 Skill Analysis:
{analysis}

Let's discuss your projects...
"""

    # ---------------------------
    # PROJECT DEEP DIVE
    # ---------------------------
    if state == CUSTOM_STATES["PROJECT_DEEP_DIVE"]:

        if not session["project_done"]:
            q = generate_project_question(session.get("projects"))
            session["project_done"] = True
            session["questions"].append(q)

            return f"""
Great — starting with your project.

{q}
"""

        prev_q = session["questions"][-1]
        eval_result = evaluate_answer(prev_q, user_input)
        session["evaluation"].append(eval_result)

        session["state"] = CUSTOM_STATES["INTERVIEW"]

        return f"""
📊 Project Evaluation:
{eval_result}

Now moving to technical questions...
"""

    # ---------------------------
    # INTERVIEW
    # ---------------------------
    if state == CUSTOM_STATES["INTERVIEW"]:

        if session["current_q"] == 0:
            q = generate_question(session)
            session["questions"].append(q)
            session["current_q"] += 1
            return f"Let's continue.\n\n{q}"

        prev_q = session["questions"][-1]
        eval_result = evaluate_answer(prev_q, user_input)
        session["evaluation"].append(eval_result)

        follow = ""
        if "Follow-up Question:" in eval_result:
            follow = eval_result.split("Follow-up Question:")[-1].strip()

        if session["current_q"] >= 3:
            session["state"] = CUSTOM_STATES["FINAL_DECISION"]
            return f"{eval_result}\n\nGenerating final result..."

        next_q = follow if follow else generate_question(session)

        session["questions"].append(next_q)
        session["current_q"] += 1

        return f"""
📊 Evaluation:
{eval_result}

➡️ Next:
{next_q}
"""

    # ---------------------------
    # FINAL
    # ---------------------------
    if state == CUSTOM_STATES["FINAL_DECISION"]:

        session["state"] = STATES["END"]
        summary = generate_summary(session)

        result = final_decision(session)

        return f"""

{summary}

📊 Detailed Evaluation:
{result}
"""

    return FALLBACK_PROMPT