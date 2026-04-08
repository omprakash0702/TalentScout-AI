# TalentScout – AI Hiring Assistant

## Tech Stack

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)


# TalentScout AI – Hiring Assistant

TalentScout AI is a full-stack recruitment assistant designed to simulate a structured hiring workflow. It combines conversational screening, resume analysis, and job-role alignment into a single system. The focus is on building a realistic, controlled hiring pipeline rather than a generic chatbot.

The application uses a Streamlit interface for user interaction and a FastAPI backend for handling logic and APIs. It is containerized with Docker and deployed on Google Cloud Run with secure secret management.

---

## Live Demo

New Deployment  
https://talentscout-v2-1006031252410.asia-south1.run.app/

Previous Version  
https://talentscout-1006031252410.asia-south1.run.app/

---

## Overview

The system guides candidates through an initial screening process similar to a recruiter-led interaction. It collects structured inputs such as domain, role, experience, and technical skills, then generates context-aware technical questions.

In parallel, the system supports resume analysis using ATS-style evaluation. It provides actionable feedback and realistic suggestions, especially tailored for entry-level candidates. A job match layer helps users understand how well their profile aligns with a target role.

Authentication and session tracking allow users to maintain continuity, revisit results, and restart flows when needed.

---

## Core Features

### Screening Workflow

The screening assistant follows a controlled flow. It collects candidate details, validates inputs, and generates technical questions based on experience level and skill set. The interaction remains focused and structured, avoiding open-ended chat.

At the end of the flow, the system produces a concise summary along with guidance for interview preparation and skill improvement.

---

### Resume Analysis (ATS-Based)

Users can upload a PDF resume, which is parsed and evaluated across key sections such as skills, projects, education, and experience. The system generates an ATS-style score and provides practical suggestions for improvement.

The evaluation is designed to be realistic and supportive, especially for freshers.

---

### Job Match Insight

The system compares resume content and user inputs against the selected job role. It provides a simple alignment signal that helps users understand how well their profile fits the role and where improvements are needed.

---

### Authentication

A lightweight authentication layer allows users to log in and maintain a session. This ensures a consistent experience across interactions.

---

### History Tracking

User interactions, including screening responses and resume analysis results, are stored using SQLite. This allows users to revisit previous sessions within the same runtime.

---

### Reset and New Sessions

Users can reset the application state at any time. This allows starting a new screening flow or uploading a new resume without interference from previous data.

---

## System Flow
```User
│
▼
Streamlit Interface
│
├── Authentication
│ └── Login / Session Start
│
├── Screening Flow
│ ├── Collect Inputs (Domain, Role, Experience, Skills)
│ ├── Validate Inputs
│ ├── Generate Questions (LLM)
│ ├── Capture Responses
│ └── Generate Summary + Guidance
│
├── Resume Analysis
│ ├── Upload Resume (PDF)
│ ├── Extract Text
│ ├── Run ATS Checks
│ ├── Generate Score
│ └── Provide Suggestions
│
├── Job Match
│ └── Compare Profile with Role Expectations
│
├── History
│ └── Store and Retrieve Previous Sessions
│
└── Reset
└── Clear Session and Restart Flow

▼
FastAPI Backend
│
├── Conversation Engine
├── Prompt Management
├── Validation Layer
├── Auth Handling
│
▼
SQLite (Session Storage)
│
▼
OpenAI API (LLM Processing)
```

---

## Architecture

The system follows a layered design.

The frontend is built with Streamlit and handles user interaction and flow control. The backend is implemented using FastAPI, managing APIs, authentication, and business logic.

Core modules handle conversation state, prompt design, and validation. SQLite is used for lightweight session storage. OpenAI APIs are used for generating intelligent responses.

Both frontend and backend run inside a single Docker container, simplifying deployment and ensuring consistency.

---

## Project Structure
```
TALENTSCOUT_AI/
│
├── backend/
│ ├── main.py
│ ├── chat.py
│ ├── core/
│ ├── db/
│ ├── routes/
│
├── ui/
├── utils/
│
├── core_old/ # previous implementation preserved
│
├── app.py # Streamlit frontend
├── Dockerfile
├── requirements.txt
├── README.md
```

---

## Deployment

The application is containerized using Docker and deployed on Google Cloud Run. Both frontend and backend run within a single container.

Sensitive data such as API keys are managed using Google Secret Manager and injected at runtime. The system is stateless and uses ephemeral storage, making it suitable for scalable deployments.

---

## Tech Stack

Frontend: Streamlit  
Backend: FastAPI  
Language: Python  
Database: SQLite  
LLM Integration: OpenAI API  
Containerization: Docker  
Cloud Platform: Google Cloud Run  
Secrets Management: Google Secret Manager  

---

## 📚 Resources & References
- Streamlit Docs
 https://docs.streamlit.io/
- OpenAI API Documentation
https://platform.openai.com/docs
- Google Cloud Run
https://cloud.google.com/run/docs
- Google Artifact Registry
https://cloud.google.com/artifact-registry/docs
- Google Secret Manager
https://cloud.google.com/secret-manager/docs
- Prompt Engineering Guide
https://www.promptingguide.ai/

## 📝 License
This project is licensed under the MIT License.
