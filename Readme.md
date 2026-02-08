# TracePoint AI - Complete Project Overview

## Executive Summary

TracePoint AI is a full-stack web application that combines AI-powered code analysis with educational features. The platform offers three main functionalities:

1. **AI Chat Assistant** - Interactive coding tutor
2. **Code Analysis Tool** - Real-time code explanation and execution
3. **Forensic Analysis** - Deep code structure and security analysis

## Architecture

### Technology Stack

**Backend:**
- Flask 3.0.0 (Web framework)
- Flask-Login 0.6.3 (Authentication)
- Flask-CORS 4.0.0 (Cross-origin requests)
- SQLite (Database)
- OpenAI API (GPT-4o-mini)
- gTTS (Text-to-speech)

**Frontend:**
- HTML5
- CSS3 (Custom styling, gradients, animations)
- Vanilla JavaScript (No frameworks)

**Security:**
- Werkzeug password hashing (PBKDF2-SHA256)
- Session management
- Input validation
- Sandboxed code execution
