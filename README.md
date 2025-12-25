<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TalentScout – AI Hiring Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px 40px;
            text-align: center;
            position: relative;
        }
        
        .header::after {
            content: '';
            position: absolute;
            bottom: -50px;
            left: 0;
            right: 0;
            height: 100px;
            background: white;
            border-radius: 100% 100% 0 0;
        }
        
        .badges {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        
        .badge {
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .badge img {
            height: 20px;
            width: 20px;
        }
        
        .hero {
            padding: 60px 40px 40px;
            text-align: center;
        }
        
        .cta-buttons {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 15px 30px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s ease;
            font-size: 16px;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-secondary {
            background: #764ba2;
            color: white;
        }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        
        .section {
            padding: 40px;
            border-bottom: 1px solid #eee;
        }
        
        .section-title {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 24px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }
        
        .feature-card {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
            transition: transform 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .flow-diagram {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin: 20px 0;
        }
        
        .flow-step {
            display: flex;
            align-items: center;
            margin: 15px 0;
            padding: 15px;
            background: white;
            border-radius: 10px;
        }
        
        .step-number {
            background: #667eea;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 20px;
            flex-shrink: 0;
        }
        
        code {
            background: #2d2d2d;
            color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            display: block;
            overflow-x: auto;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
        }
        
        .terminal {
            background: #2d2d2d;
            color: #00ff00;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
        }
        
        .tech-stack {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin: 20px 0;
        }
        
        .tech-item {
            background: #667eea;
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: 600;
        }
        
        .footer {
            background: #2d2d2d;
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 0 0 20px 20px;
        }
        
        @media (max-width: 768px) {
            .container {
                border-radius: 10px;
            }
            
            .header, .section {
                padding: 30px 20px;
            }
            
            .cta-buttons {
                flex-direction: column;
                align-items: center;
            }
            
            .btn {
                width: 100%;
                justify-content: center;
            }
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 TalentScout</h1>
            <h2>AI Hiring Assistant</h2>
            <div class="badges">
                <div class="badge"><i class="fab fa-streamlit"></i> Streamlit</div>
                <div class="badge"><i class="fab fa-openai"></i> OpenAI</div>
                <div class="badge"><i class="fab fa-docker"></i> Docker</div>
                <div class="badge"><i class="fab fa-google"></i> Google Cloud</div>
            </div>
        </div>
        
        <div class="hero">
            <p class="subtitle">AI-powered recruitment assistant for initial candidate screening and resume ATS evaluation</p>
            <div class="cta-buttons">
                <a href="https://talentscout-1006031252410.asia-south1.run.app/" class="btn btn-primary" target="_blank">
                    <i class="fas fa-rocket"></i> Live Demo
                </a>
                <a href="https://github.com/omprakash0702/TalentScout" class="btn btn-secondary" target="_blank">
                    <i class="fab fa-github"></i> Source Code
                </a>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title"><i class="fas fa-bullseye"></i> Project Overview</h2>
            <p>TalentScout simulates a real-world recruitment workflow by combining structured candidate intake, context-aware technical screening using LLMs, resume ATS scanning with realistic fresher handling, practical post-screening guidance, and secure, scalable cloud deployment.</p>
            <div class="flow-diagram">
                <div class="flow-step">
                    <div class="step-number">1</div>
                    <div>Candidate interacts with AI Assistant via Streamlit UI</div>
                </div>
                <div class="flow-step">
                    <div class="step-number">2</div>
                    <div>LLM processes structured screening questions based on domain & experience</div>
                </div>
                <div class="flow-step">
                    <div class="step-number">3</div>
                    <div>Resume undergoes ATS scanning with section-wise analysis</div>
                </div>
                <div class="flow-step">
                    <div class="step-number">4</div>
                    <div>Results & recommendations delivered to candidate</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title"><i class="fas fa-star"></i> Key Features</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <h3><i class="fas fa-comments"></i> Live Screening Assistant</h3>
                    <p>Recruiter-led conversation with Domain → Job Role → Experience → Tech Stack flow. Experience-aware technical question generation with strict scope control.</p>
                </div>
                <div class="feature-card">
                    <h3><i class="fas fa-file-pdf"></i> Resume ATS Scan</h3>
                    <p>PDF resume upload with section-aware ATS checks (Summary, Experience, Projects, Skills, Education). Realistic fresher-friendly scoring with actionable improvement suggestions.</p>
                </div>
                <div class="feature-card">
                    <h3><i class="fas fa-graduation-cap"></i> Post-Screening Guidance</h3>
                    <p>Interview preparation tips, skill improvement roadmap, and resume improvement advice with controlled intent-based responses.</p>
                </div>
                <div class="feature-card">
                    <h3><i class="fas fa-cloud"></i> Production Deployment</h3>
                    <p>Dockerized Streamlit app deployed on Google Cloud Run with secrets managed via Google Secret Manager and scale-to-zero enabled.</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title"><i class="fas fa-code"></i> Tech Stack</h2>
            <div class="tech-stack">
                <div class="tech-item">Streamlit (Frontend)</div>
                <div class="tech-item">Python (Backend)</div>
                <div class="tech-item">OpenAI GPT-4/3.5 (LLM)</div>
                <div class="tech-item">Docker (Containerization)</div>
                <div class="tech-item">Google Cloud Run (Deployment)</div>
                <div class="tech-item">Google Secret Manager (Secrets)</div>
                <div class="tech-item">Google Artifact Registry</div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title"><i class="fas fa-terminal"></i> Quick Deployment</h2>
            <div class="terminal">
                <p>$ docker build -t talentscout .</p>
                <p>$ docker tag talentscout asia-south1-docker.pkg.dev/YOUR-PROJECT/talentscout:latest</p>
                <p>$ docker push asia-south1-docker.pkg.dev/YOUR-PROJECT/talentscout:latest</p>
                <p>$ gcloud run deploy talentscout --image asia-south1-docker.pkg.dev/YOUR-PROJECT/talentscout:latest --region asia-south1 --allow-unauthenticated --set-secrets OPENAI_API_KEY=OPENAI_API_KEY:latest</p>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title"><i class="fas fa-project-diagram"></i> Project Structure</h2>
            <code>Talentscout/
├── app.py                      # Main Streamlit application
├── core/
│   ├── conversation.py         # Screening state machine
│   ├── llm.py                  # OpenAI client & API calls
│   ├── prompts.py              # All LLM prompts
│   ├── validators.py           # Input validation logic
│   └── ats_checks.py           # ATS scoring algorithms
├── utils/
│   ├── resume_parser.py        # PDF text extraction
│   └── constants.py            # State definitions
├── ui/
│   └── styles.py               # Custom styling
├── Dockerfile                  # Container configuration
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
└── README.md                   # Documentation</code>
        </div>
        
        <div class="footer">
            <p>Made with ❤️ by <strong>Omprakash</strong></p>
            <div style="margin-top: 15px;">
                <a href="https://github.com/omprakash0702/TalentScout" style="color: white; margin: 0 10px;" target="_blank">
                    <i class="fab fa-github fa-2x"></i>
                </a>
                <a href="https://talentscout-1006031252410.asia-south1.run.app/" style="color: white; margin: 0 10px;" target="_blank">
                    <i class="fas fa-external-link-alt fa-2x"></i>
                </a>
            </div>
            <p style="margin-top: 20px; font-size: 14px; color: #aaa;">MIT License © 2024 TalentScout AI</p>
        </div>
    </div>

    <script>
        // Add smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
        
        // Add animation to feature cards on scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);
        
        document.querySelectorAll('.feature-card').forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(card);
        });
    </script>
</body>
</html>
