import fitz  # PyMuPDF
import json
import re
from backend.core.llm import call_llm


# ---------------------------
# STEP 1: EXTRACT TEXT (KEEP YOUR VERSION)
# ---------------------------
def extract_resume_text(file) -> str:
    text = ""

    # reset pointer (important for Streamlit uploads)
    file.seek(0)

    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    return text.strip()


# ---------------------------
# STEP 2: SAFE JSON PARSER
# ---------------------------
def safe_json_loads(response: str):
    try:
        return json.loads(response)
    except:
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
    return {}


# ---------------------------
# STEP 3: NORMALIZATION
# ---------------------------
def normalize_data(data: dict):

    # --- Experience ---
    exp = str(data.get("Years of Experience", "0")).lower()

    if "fresher" in exp or "student" in exp:
        exp_val = "0"
    else:
        match = re.search(r"\d+(\.\d+)?", exp)
        exp_val = match.group() if match else "0"

    # --- Skills ---
    skills = data.get("Skills", "")
    if isinstance(skills, list):
        skills = ", ".join(skills)

    # --- Projects ---
    projects = data.get("Projects", [])
    if not isinstance(projects, list):
        projects = []

    return {
        "Full Name": data.get("Full Name", "").strip(),
        "Email Address": data.get("Email Address", "").strip(),
        "Job Role": data.get("Job Role", "").strip(),
        "Years of Experience": exp_val,
        "Skills": skills.strip(),
        "Projects": projects,
    }


# ---------------------------
# STEP 4: MAIN PARSER
# ---------------------------
def parse_resume(text: str):

    prompt = f"""
You are a strict resume parser.

Extract ONLY these fields in VALID JSON:

- Full Name
- Email Address
- Job Role (best guess)
- Years of Experience (number only)
- Skills (comma separated string)
- Projects (list of strings)

Rules:
- If fresher → experience = 0
- Do NOT hallucinate
- Keep values realistic
- Output ONLY JSON (no explanation)

Resume:
{text[:4000]}
"""

    response = call_llm([{"role": "user", "content": prompt}])

    parsed = safe_json_loads(response)

    if not parsed:
        return {
            "Full Name": "",
            "Email Address": "",
            "Job Role": "",
            "Years of Experience": "0",
            "Skills": "",
            "Projects": [],
        }

    return normalize_data(parsed)