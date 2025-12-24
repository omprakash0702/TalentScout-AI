import os
from datetime import date
from dotenv import load_dotenv

# Load env FIRST
load_dotenv()

import streamlit as st
from utils.constants import STATES
from core.conversation import handle_conversation
from ui.styles import apply_global_styles
from utils.resume_parser import extract_resume_text
from core.ats_checks import basic_ats_checks
from core.llm import call_llm
from core.prompts import RESUME_REVIEW_PROMPT

# ---------- STREAMLIT CONFIG ----------
st.set_page_config(
    page_title="TalentScout – AI Hiring Assistant",
    layout="centered",
)

apply_global_styles()

st.title("TalentScout – AI Hiring Assistant")
st.caption(
    "AI-powered recruitment assistant for initial screening and resume evaluation."
)

# ---------- MODE SELECTION ----------
mode = st.sidebar.radio(
    "Select Mode",
    ["Live Screening Chat", "Resume Scan (ATS Review)"],
)

# =====================================================
# 🔹 MODE 1: LIVE SCREENING CHAT
# =====================================================
if mode == "Live Screening Chat":

    if "state" not in st.session_state:
        st.session_state.state = STATES["GREETING"]
        st.session_state.messages = []
        st.session_state.candidate_data = {}

    # ---------- STRUCTURED INPUTS ----------
    with st.expander("📋 Candidate Details (Structured)", expanded=True):

        st.session_state.candidate_data["primary_domain"] = st.selectbox(
            "Primary Domain",
            [
                "AI / Machine Learning",
                "Backend Engineering",
                "Frontend Engineering",
                "Data Science / Analytics",
                "DevOps / Cloud",
            ],
        )

        st.session_state.candidate_data["country_code"] = st.selectbox(
            "Country Code",
            ["+91 (India)", "+1 (USA)", "+44 (UK)", "+61 (Australia)"],
        )

        st.session_state.candidate_data["phone_number"] = st.text_input(
            "Phone Number (10 digits)",
            placeholder="e.g. 7814842689"
        )

        st.session_state.candidate_data["dob"] = st.date_input(
            "Date of Birth",
            min_value=date(1960, 1, 1),
            max_value=date.today(),
            value=date(2000, 1, 1),
        )

    # ---------- AUTO GREETING ----------
    if st.session_state.state == STATES["GREETING"] and not st.session_state.messages:
        greeting = handle_conversation("", st.session_state)
        st.session_state.messages.append(
            {"role": "assistant", "content": greeting}
        )

    # ---------- CHAT ----------
    user_input = st.chat_input("Type your response here...")

    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )
        response = handle_conversation(user_input, st.session_state)
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# =====================================================
# 🔹 MODE 2: RESUME SCAN (ATS + REVIEW)  ✅ FIXED
# =====================================================
else:
    st.subheader("📄 Resume Scan (ATS Review)")

    resume_file = st.file_uploader(
        "Upload your resume (PDF only)",
        type=["pdf"]
    )

    if resume_file:
        resume_text = extract_resume_text(resume_file)
        ats_result = basic_ats_checks(resume_text)

        st.subheader("ATS Compatibility Score")
        st.progress(ats_result["score"] / 100)
        st.write(f"**Score:** {ats_result['score']} / 100")

        st.subheader("ATS Section Check")
        for k, v in ats_result["checks"].items():
            st.write(f"- {k.replace('_', ' ').title()}: {'✅' if v else '❌'}")

        with st.spinner("Reviewing resume and generating suggestions..."):
            prompt = RESUME_REVIEW_PROMPT.format(
                resume_text=resume_text[:3500],
                ats_checks=ats_result
            )
            review = call_llm([{"role": "user", "content": prompt}])

        st.subheader("AI Resume Review & Suggestions")
        st.markdown(review)
