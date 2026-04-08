import os
import uuid
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import requests

st.set_page_config(page_title="TalentScout AI", layout="centered")

# ================= AUTH =================
st.sidebar.subheader("🔐 Authentication")

if "token" not in st.session_state:
    st.session_state.token = None

if "session_mode" not in st.session_state:
    st.session_state.session_mode = None

auth_mode = st.sidebar.radio("Select", ["Login", "Register"])

email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Submit"):

    url = f"http://127.0.0.1:8000/auth/{auth_mode.lower()}"

    try:
        res = requests.post(url, json={"email": email, "password": password})
        data = res.json()

        if auth_mode == "Login":
            if "access_token" in data:
                st.session_state.token = data["access_token"]
                st.session_state.session_mode = None
                st.session_state.messages = []

                # ADDED: ensure fresh backend session
                st.session_state.user_id = str(uuid.uuid4())

                st.sidebar.success("✅ Logged in")
            else:
                st.sidebar.error("❌ Login failed")

        else:
            st.sidebar.success("✅ Registered successfully")

    except Exception as e:
        st.sidebar.error(f"❌ Auth failed: {e}")

# LOGIN STATUS + LOGOUT
if st.session_state.token:
    st.sidebar.success("🟢 Logged in")

    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.session_mode = None
        st.rerun()

    # ================= SESSION MODE =================
    if st.session_state.session_mode is None:
        st.sidebar.subheader("🧠 Session Mode")

        col1, col2 = st.sidebar.columns(2)

        if col1.button("Continue"):
            st.session_state.session_mode = "continue"

        if col2.button("New"):
            st.session_state.session_mode = "new"
            st.session_state.messages = []
            st.session_state.parsed_resume = None
            st.session_state.resume_sent = False
            st.session_state.raw_text = ""

            # ADDED: force new backend session
            st.session_state.user_id = str(uuid.uuid4())

            st.rerun()

else:
    st.sidebar.warning("🔴 Not logged in")

# ================= IMPORTS =================
from ui.styles import apply_global_styles
from utils.resume_parser import extract_resume_text, parse_resume
from core_old.llm import call_llm
from core_old.prompts import RESUME_REVIEW_PROMPT

# ---------- STYLES ----------
apply_global_styles()

# ---------- SESSION ----------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "parsed_resume" not in st.session_state:
    st.session_state.parsed_resume = None

if "resume_sent" not in st.session_state:
    st.session_state.resume_sent = False

if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""

# ---------- RESET (FIXED) ----------
if st.sidebar.button("🔄 Reset Session"):
    st.session_state.messages = []
    st.session_state.parsed_resume = None
    st.session_state.resume_sent = False
    st.session_state.raw_text = ""

    # ADDED: critical fix for backend session
    st.session_state.user_id = str(uuid.uuid4())

    st.rerun()

# ---------- HEADER ----------
st.title("TalentScout – AI Hiring Assistant")
st.caption("AI-powered recruitment assistant for real-time screening")

# PROTECTION
if not st.session_state.token:
    st.warning("⚠️ Please login to use the app")
    st.stop()

# ---------- MODE ----------
mode = st.sidebar.radio(
    "Choose Feature",
    ["Screening", "Resume Analysis", "Job Match", "History"]
)

# =====================================================
# RESUME UPLOAD
# =====================================================
st.subheader("📄 Upload Resume")

resume_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

if resume_file and not st.session_state.parsed_resume:
    with st.spinner("Parsing resume..."):
        text = extract_resume_text(resume_file)
        parsed = parse_resume(text)

        st.session_state.parsed_resume = parsed
        st.session_state.raw_text = text
        st.session_state.resume_sent = False

    st.success("✅ Resume parsed successfully")

    with st.expander("📊 Extracted Resume Data"):
        st.json(parsed)

if st.button("🆕 Start with New Resume"):
    st.session_state.parsed_resume = None
    st.session_state.raw_text = ""
    st.session_state.resume_sent = False
    st.session_state.messages = []

    # ADDED: ensure fresh backend flow
    st.session_state.user_id = str(uuid.uuid4())

    st.rerun()

# =====================================================
# SCREENING MODE
# =====================================================
if mode == "Screening":

    def call_api(message):
        payload = {
            "user_id": st.session_state.user_id,
            "message": message,
            "resume_data": None,
        }

        if st.session_state.parsed_resume and not st.session_state.resume_sent:
            payload["resume_data"] = st.session_state.parsed_resume
            st.session_state.resume_sent = True

        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        try:
            res = requests.post(
                "http://127.0.0.1:8000/chat",
                json=payload,
                headers=headers
            )
            return res.json().get("response", "⚠️ Backend error")
        except Exception as e:
            return f"⚠️ Error: {e}"

    if not st.session_state.messages:
        first = call_api("")
        st.session_state.messages.append({
            "role": "assistant",
            "content": first
        })

    user_input = st.chat_input("Type your response...")

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        response = call_api(user_input)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# =====================================================
# RESUME ANALYSIS MODE
# =====================================================
elif mode == "Resume Analysis":

    if not st.session_state.parsed_resume:
        st.warning("⚠️ Please upload a resume first.")
    else:

        def basic_ats_score(text):
            checks = {
                "Has Summary": "summary" in text.lower(),
                "Has Experience": "experience" in text.lower(),
                "Has Projects": "project" in text.lower(),
                "Has Skills": "skill" in text.lower(),
                "Has Education": "education" in text.lower(),
            }

            score = sum(checks.values()) * 20
            return score, checks

        score, checks = basic_ats_score(st.session_state.raw_text)

        st.subheader("📊 ATS Compatibility Score")
        st.progress(score / 100)
        st.write(f"Score: {score}/100")

        st.subheader("📄 Section Check")
        for k, v in checks.items():
            st.write(f"{k}: {'✅' if v else '❌'}")

        with st.spinner("Analyzing resume..."):
            prompt = RESUME_REVIEW_PROMPT.format(
                resume_text=st.session_state.raw_text[:3500],
                ats_checks=checks
            )

            review = call_llm([{"role": "user", "content": prompt}])

        st.subheader("🧠 AI Resume Review")
        st.markdown(review)

# =====================================================
# JOB MATCH MODE
# =====================================================
elif mode == "Job Match":

    if not st.session_state.parsed_resume:
        st.warning("⚠️ Please upload a resume first.")
    else:

        st.subheader("🎯 Job Match & Career Fit")

        with st.spinner("Analyzing job fit..."):
            prompt = f"""
Resume:
{st.session_state.raw_text[:3500]}

Return top 3 roles with:
- Role
- Match Score (0-100%)
- Reason for Score
- Key Strengths
- Missing Skills
"""

            result = call_llm([{"role": "user", "content": prompt}])

        st.markdown(result)

# =====================================================
# HISTORY MODE
# =====================================================
elif mode == "History":

    st.subheader("📊 Your Screening History")

    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    # ADDED: clear history button
    if st.button("Clear History"):
        try:
            requests.delete(
                "http://127.0.0.1:8000/history",
                headers=headers
            )
            st.success("History cleared")
            st.rerun()
        except:
            st.error("Failed to clear history")

    try:
        res = requests.get(
            "http://127.0.0.1:8000/history",
            headers=headers
        )

        st.write("Status:", res.status_code)

        data = res.json()

        if not data:
            st.info("No history found.")
        else:
            for item in data:
                with st.container():
                    st.markdown("-----")
                    st.write(f"📝 Resume: {item['resume'][:100]}...")
                    st.write(f"📊 Score: {item['score']}")
                    st.write(f"💬 Feedback: {item['feedback']}")
                    st.write(f"⏱️ Date: {item['created_at']}")

    except Exception as e:
        st.error(f"❌ Failed to fetch history: {e}")