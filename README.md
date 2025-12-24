# TalentScout – AI Hiring Assistant

TalentScout is an AI-powered recruitment assistant designed to simulate real-world hiring workflows.
It supports candidate screening, technical assessment, and ATS-based resume evaluation with realistic,
fresher-friendly guidance.

---

## Features

- Structured candidate intake (domain, role, experience, DOB)
- Context-aware screening conversation
- Tech-stack–based interview question generation
- Resume ATS scan with section detection
- Practical resume improvement suggestions
- Post-screening guidance (interview prep, skills, resume advice)
- Privacy-first design (no data persistence)

---

## Architecture

- Frontend & Backend: Streamlit
- LLM: OpenAI (GPT-4o-mini)
- Resume Parsing: PDF text extraction
- State Handling: Session-based (no database)
- Deployment: AWS App Runner (Docker)

---

## Data Handling & Privacy

- No candidate data is stored permanently
- Resume files are processed in-memory per session
- No database or data folder is used for real candidates
- Sample data is provided for documentation only

---

## Sample Candidate Data

`data/sample_candidate.json` demonstrates the expected data schema for candidate information.
It is used only for documentation and testing purposes.

---

## Why No Database?

This project simulates real-time recruitment screening.
Persisting candidate data without consent is avoided to align with privacy best practices.

---

## Deployment

The application is containerized using Docker and deployed on AWS App Runner.
App Runner was chosen for its simplicity, scalability, and native support for web applications.

---

## How to Run Locally

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
