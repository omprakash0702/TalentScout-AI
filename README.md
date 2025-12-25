📌 TalentScout – AI Hiring Assistant

AI-powered recruitment assistant for initial candidate screening and resume ATS evaluation, built with Streamlit, LLMs, Docker, and Google Cloud Run.

🔗 Live Demo: (Cloud Run URL)
🔗 Source Code: (GitHub repo)

🚀 Project Overview

TalentScout simulates a real-world recruitment workflow by combining:

Structured candidate intake (ATS-style)

Context-aware technical screening using LLMs

Resume ATS scanning with realistic fresher handling

Practical post-screening guidance (interview, skills, resume)

Secure, scalable cloud deployment

This project focuses on correct use of LLMs, not generic chatbot behavior.

🎯 Key Features
🔹 Live Screening Assistant

Recruiter-led conversation (assistant starts first)

Domain → Job Role → Experience → Tech Stack flow

Experience-aware technical question generation

Strict scope control (not open-ended chat)

🔹 Resume Scan (ATS Review)

PDF resume upload

Section-aware ATS checks (Summary, Experience, Projects, Skills, Education, Achievements)

Realistic scoring (fresher-friendly)

Actionable improvement suggestions (no toxic expectations)

🔹 Post-Screening Guidance

Interview preparation tips

Skill improvement roadmap

Resume improvement advice

Controlled intent-based responses

🔹 Production Deployment

Dockerized Streamlit app

Deployed on Google Cloud Run

Secrets managed via Google Secret Manager

Scale-to-zero enabled

🧠 Application Architecture
🔷 High-Level Architecture (Visual)
User (Browser)
    |
    v
Streamlit UI (app.py)
    |
    ├── Live Screening Flow
    |      ├── conversation.py
    |      ├── validators.py
    |      ├── prompts.py
    |      └── llm.py  → OpenAI API
    |
    ├── Resume Scan Flow
    |      ├── resume_parser.py
    |      ├── ats_checks.py
    |      ├── prompts.py
    |      └── llm.py  → OpenAI API
    |
    v
Google Cloud Run
    ├── Docker Container
    ├── Secret Manager (OPENAI_API_KEY)
    ├── HTTPS + Scaling

🔄 End-to-End Flow
1️⃣ Candidate Screening

Assistant greets candidate

Collects structured information (domain, role, experience)

Validates inputs (email, experience, tech stack)

Generates tailored technical questions

Produces candidate summary

Offers post-screening guidance

2️⃣ Resume ATS Scan

User uploads PDF resume

Resume text extracted

ATS section checks performed

ATS score calculated

LLM generates realistic review & suggestions

📂 Project Structure & File Responsibilities
Talentscout_ai/
│
├── app.py
│   └── Main Streamlit UI
│       • Mode selection (Chat / Resume Scan)
│       • Handles user interaction
│       • Orchestrates application flow
│
├── core/
│   ├── conversation.py
│   │   • Screening state machine
│   │   • Input validation logic
│   │   • LLM interaction control
│   │
│   ├── llm.py
│   │   • Centralized OpenAI client
│   │   • Handles API calls safely
│   │
│   ├── prompts.py
│   │   • All LLM prompts
│   │   • Technical questions
│   │   • Resume review logic
│   │
│   ├── validators.py
│   │   • Email, name, experience, tech stack validation
│   │
│   ├── ats_checks.py
│   │   • Section-aware ATS checks
│   │   • Fresher-safe scoring
│
├── utils/
│   ├── resume_parser.py
│   │   • PDF resume text extraction
│   │
│   ├── constants.py
│   │   • State definitions
│   │   • Exit keywords
│
├── ui/
│   ├── styles.py
│   │   • Custom Streamlit styling
│
├── Dockerfile
│   └── Container configuration
│
├── requirements.txt
│   └── Python dependencies
│
├── .env (local only)
│   └── Environment variables (not committed)
│
└── README.md

☁️ Deployment (Google Cloud Run)
Deployment Highlights

Dockerized Streamlit app

Image stored in Google Artifact Registry

Secrets injected via Google Secret Manager

Public HTTPS endpoint

Automatic scaling (scale-to-zero)

Deployment Commands (Summary)
docker build -t talentscout .
docker tag talentscout asia-south1-docker.pkg.dev/PROJECT/REPO/talentscout:latest
docker push asia-south1-docker.pkg.dev/PROJECT/REPO/talentscout:latest

gcloud run deploy talentscout \
  --image asia-south1-docker.pkg.dev/PROJECT/REPO/talentscout:latest \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-secrets OPENAI_API_KEY=OPENAI_API_KEY:latest

🔐 Security & Best Practices

❌ No API keys in code or GitHub

✅ Secrets managed via GCP Secret Manager

✅ .env ignored in version control

✅ LLM calls guarded against Streamlit reruns

✅ Minimal permissions used

📦 Tech Stack

Frontend: Streamlit

Backend Logic: Python

LLM: OpenAI (Responses API)

Containerization: Docker

Cloud: Google Cloud Run

Secrets: Google Secret Manager

Registry: Google Artifact Registry

📚 Resources & References

Streamlit Docs
https://docs.streamlit.io/

OpenAI API Documentation
https://platform.openai.com/docs

Google Cloud Run
https://cloud.google.com/run/docs

Google Artifact Registry
https://cloud.google.com/artifact-registry/docs

Google Secret Manager
https://cloud.google.com/secret-manager/docs

Prompt Engineering Guide
https://www.promptingguide.ai/

📝 License

This project is licensed under the MIT License.

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
