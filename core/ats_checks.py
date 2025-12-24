import re

SECTION_HEADERS = {
    "summary": ["summary", "profile"],
    "experience": ["experience", "work experience", "employment", "internship", "internships"],
    "projects": ["projects", "academic projects"],
    "skills": ["skills", "technical skills"],
    "education": ["education"],
    "achievements": ["achievements", "accomplishments"],
}

def has_section(text: str, section_keywords: list) -> bool:
    text = text.lower()
    for keyword in section_keywords:
        # look for section header pattern
        pattern = rf"\n\s*{keyword}\s*\n|{keyword.upper()}|{keyword.title()}"
        if re.search(pattern, text):
            return True
    return False

def basic_ats_checks(resume_text: str) -> dict:
    checks = {
        "has_summary": has_section(resume_text, SECTION_HEADERS["summary"]),
        "has_experience": has_section(resume_text, SECTION_HEADERS["experience"]),
        "has_projects": has_section(resume_text, SECTION_HEADERS["projects"]),
        "has_skills": has_section(resume_text, SECTION_HEADERS["skills"]),
        "has_education": has_section(resume_text, SECTION_HEADERS["education"]),
        "has_achievements": has_section(resume_text, SECTION_HEADERS["achievements"]),
    }

    score = (sum(checks.values()) / len(checks)) * 100

    return {
        "score": round(score, 1),
        "checks": checks,
    }
