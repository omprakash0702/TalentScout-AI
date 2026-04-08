# TalentScout AI – Hiring Assistant

## Tech Stack

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

---

TalentScout AI is a full-stack recruitment assistant designed to simulate a structured hiring workflow. It combines conversational screening, resume analysis, and job-role alignment into a single system. The focus is on building a realistic, controlled hiring pipeline rather than a generic chatbot.

The application uses a Streamlit interface for interaction and a FastAPI backend for handling logic and APIs. It is containerized with Docker and deployed on Google Cloud Run with secure secret management.

---

## Live Demo

New Deployment  
https://talentscout-v2-1006031252410.asia-south1.run.app/

Previous Version  
https://talentscout-1006031252410.asia-south1.run.app/

---

## Overview

The system guides candidates through a structured screening process similar to a recruiter-led interaction. It collects inputs such as domain, role, experience, and technical skills, then generates context-aware technical questions.

Alongside screening, the system supports resume analysis using ATS-style evaluation. It provides actionable feedback and realistic suggestions, especially for entry-level candidates. A job match layer helps users understand alignment with target roles.

Authentication and session tracking allow users to maintain continuity, revisit results, and restart flows when needed.

---

## Features

### Screening Workflow

The screening assistant follows a structured flow. It collects candidate details, validates inputs, and generates technical questions based on experience level and skills. The interaction remains focused and produces a concise summary with guidance.

---

### Resume Analysis

Users can upload a PDF resume for evaluation. The system extracts content, analyzes key sections, and generates an ATS-style score with practical suggestions.

---

### Job Match

The system compares candidate profile data with selected job roles and provides a simple alignment insight to highlight strengths and gaps.

---

### Authentication

A lightweight authentication system allows users to log in and maintain session continuity.

---

### History Tracking

User interactions and results are stored using SQLite, allowing users to revisit previous sessions during runtime.

---

### Reset and New Sessions

Users can reset the system at any point to start a new screening or resume analysis without interference from previous data.

---

## System Flow
```
User
│
▼
Streamlit Interface
│
├── Authentication
│ └── Login / Session Start
│
├── Screening Flow
│ ├── Collect Inputs
│ ├── Validate Inputs
│ ├── Generate Questions (LLM)
│ └── Summary + Guidance
│
├── Resume Analysis
│ ├── Upload Resume
│ ├── Extract Text
│ ├── ATS Checks
│ └── Suggestions
│
├── Job Match
│ └── Role Alignment
│
├── History
│ └── Store / Retrieve Sessions
│
└── Reset
└── Start Fresh Session

▼
FastAPI Backend
│
├── Conversation Logic
├── Prompt Handling
├── Validation
├── Authentication
│
▼
SQLite Storage
│
▼
OpenAI API
```

---

## Screenshots

### Screening Interface
![Screening](screenshots/screening.png)

### Resume Analysis
![Resume](screenshots/resume.png)

### Job Match Output
![Job Match](screenshots/job_match.png)

### History and Session
![History](screenshots/history.png)

---

## Architecture

The system follows a layered design.

Streamlit handles user interaction and flow control. FastAPI manages backend logic and APIs. Core modules handle conversation, prompts, and validation. SQLite stores session data. OpenAI powers intelligent responses.

Both frontend and backend run inside a single Docker container, simplifying deployment.

---

## Project Structure
```
TALENTSCOUT_AI/
│
├── backend/
│ ├── main.py # FastAPI backend
│ ├── chat.py
│ ├── core/
│ ├── db/
│ ├── routes/
│
├── ui/
├── utils/
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


## License

This project is licensed under the MIT License.
