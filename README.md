# TalentScout – AI Hiring Assistant

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

AI-powered recruitment assistant for initial candidate screening and resume ATS evaluation, built with Streamlit, LLMs, Docker, and Google Cloud Run.

## 🔗 Live Links

- **Live Demo:** [https://talentscout-ai-xxxxx-uw.a.run.app]((https://talentscout-1006031252410.asia-south1.run.app/))
- **Source Code:** [https://github.com/yourusername/talentscout-ai]((https://github.com/omprakash0702/TalentScout-A))

## 🚀 Project Overview

TalentScout simulates a real-world recruitment workflow by combining:
- Structured candidate intake (ATS-style)
- Context-aware technical screening using LLMs
- Resume ATS scanning with realistic fresher handling
- Practical post-screening guidance (interview, skills, resume)
- Secure, scalable cloud deployment

> **Focus:** Correct use of LLMs for recruitment workflows, not generic chatbot behavior.

## 🎯 Key Features

### 🔹 Live Screening Assistant
- Recruiter-led conversation (assistant starts first)
- Domain → Job Role → Experience → Tech Stack flow
- Experience-aware technical question generation
- Strict scope control (not open-ended chat)

### 🔹 Resume Scan (ATS Review)
- PDF resume upload
- Section-aware ATS checks (Summary, Experience, Projects, Skills, Education, Achievements)
- Realistic scoring (fresher-friendly)
- Actionable improvement suggestions (no toxic expectations)

### 🔹 Post-Screening Guidance
- Interview preparation tips
- Skill improvement roadmap
- Resume improvement advice
- Controlled intent-based responses

### 🔹 Production Deployment
- Dockerized Streamlit app
- Deployed on Google Cloud Run
- Secrets managed via Google Secret Manager
- Scale-to-zero enabled

## 🧠 Application Architecture

### 🔷 High-Level Architecture
<img width="6778" height="1603" alt="deepseek_mermaid_20251225_e2bad9" src="https://github.com/user-attachments/assets/8065ff02-5553-4d49-a65a-1d45d9fcbcc5" />


### 🔄 End-to-End Flow

#### 1️⃣ Candidate Screening
1. Assistant greets candidate
2. Collects structured information (domain, role, experience)
3. Validates inputs (email, experience, tech stack)
4. Generates tailored technical questions
5. Produces candidate summary
6. Offers post-screening guidance

#### 2️⃣ Resume ATS Scan
1. User uploads PDF resume
2. Resume text extracted
3. ATS section checks performed
4. ATS score calculated
5. LLM generates realistic review & suggestions

## 📂 Project Structure
Talentscout_ai/
│
├── app.py
│ └── Main Streamlit UI
│ • Mode selection (Chat / Resume Scan)
│ • Handles user interaction
│ • Orchestrates application flow
│
├── core/
│ ├── conversation.py
│ │ • Screening state machine
│ │ • Input validation logic
│ │ • LLM interaction control
│ │
│ ├── llm.py
│ │ • Centralized OpenAI client
│ │ • Handles API calls safely
│ │
│ ├── prompts.py
│ │ • All LLM prompts
│ │ • Technical questions
│ │ • Resume review logic
│ │
│ ├── validators.py
│ │ • Email, name, experience, tech stack validation
│ │
│ ├── ats_checks.py
│ │ • Section-aware ATS checks
│ │ • Fresher-safe scoring
│
├── utils/
│ ├── resume_parser.py
│ │ • PDF resume text extraction
│ │
│ ├── constants.py
│ │ • State definitions
│ │ • Exit keywords
│
├── ui/
│ ├── styles.py
│ │ • Custom Streamlit styling
│
├── Dockerfile
│ └── Container configuration
│
├── requirements.txt
│ └── Python dependencies
│
├── .env (local only)
│ └── Environment variables (not committed)
│
└── README.md


## ☁️ Deployment (Google Cloud Run)

### Deployment Highlights
- Dockerized Streamlit app
- Image stored in Google Artifact Registry
- Secrets injected via Google Secret Manager
- Public HTTPS endpoint
- Automatic scaling (scale-to-zero)

### Deployment Commands

```bash
# Build and tag Docker image
docker build -t talentscout .
docker tag talentscout asia-south1-docker.pkg.dev/PROJECT/REPO/talentscout:latest

# Push to Artifact Registry
docker push asia-south1-docker.pkg.dev/PROJECT/REPO/talentscout:latest

# Deploy to Cloud Run
gcloud run deploy talentscout \
  --image asia-south1-docker.pkg.dev/PROJECT/REPO/talentscout:latest \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-secrets OPENAI_API_KEY=OPENAI_API_KEY:latest
```

