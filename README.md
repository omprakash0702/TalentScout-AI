# README.md

```markdown
# TalentScout – AI Hiring Assistant

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

AI-powered recruitment assistant for initial candidate screening and resume ATS evaluation, built with Streamlit, LLMs, Docker, and Google Cloud Run.

## 🔗 Live Links

- **Live Demo:** [https://talentscout-ai-xxxxx-uw.a.run.app](https://talentscout-ai-xxxxx-uw.a.run.app)
- **Source Code:** [https://github.com/yourusername/talentscout-ai](https://github.com/yourusername/talentscout-ai)

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

```
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
```

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

```
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
```

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

## 🔐 Security & Best Practices

### ✅ Implemented
- Secrets managed via GCP Secret Manager
- `.env` ignored in version control
- LLM calls guarded against Streamlit reruns
- Minimal permissions used

### ❌ Avoided
- No API keys in code or GitHub
- No hardcoded credentials
- No excessive permissions

## 📦 Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend Logic | Python |
| LLM | OpenAI (Responses API) |
| Containerization | Docker |
| Cloud Runtime | Google Cloud Run |
| Secrets Management | Google Secret Manager |
| Container Registry | Google Artifact Registry |

## 📚 Resources & References

- **Streamlit Docs:** https://docs.streamlit.io/
- **OpenAI API Documentation:** https://platform.openai.com/docs
- **Google Cloud Run:** https://cloud.google.com/run/docs
- **Google Artifact Registry:** https://cloud.google.com/artifact-registry/docs
- **Google Secret Manager:** https://cloud.google.com/secret-manager/docs
- **Prompt Engineering Guide:** https://www.promptingguide.ai/

## 📝 License

This project is licensed under the MIT License.

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

**Note:** Replace the placeholder URLs with your actual deployment URLs before use. Update the project name, region, and GCP project details in deployment commands as needed.
```

**How to use this file:**
1. Save this content as `README.md` in your project root
2. Replace placeholder URLs with your actual URLs
3. Update project-specific details in deployment commands
4. Use as your main project documentation
