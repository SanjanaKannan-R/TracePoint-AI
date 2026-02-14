# TracePoint AI - Complete Project Overview
**AI-powered code analysis and learning platform** 🤖

## Executive Summary

TracePoint AI is a full-stack web application that combines AI-powered code analysis with educational features. The platform offers three main functionalities:

1. **AI Chat Assistant** - Interactive coding tutor
2. **Code Analysis Tool** - Real-time code explanation and execution
3. **Forensic Analysis** - Deep code structure and security analysis

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


> **AI-powered code analysis and learning platform** 🤖

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://openai.com)

---

## 📋 What is TracePoint AI?

TracePoint AI is an educational platform that helps you learn coding through:
- 💬 **AI Chat** - Ask programming questions and get instant answers
- 🔍 **Code Analysis** - Understand and run your code with AI explanations
- 🕵️ **Forensic Tool** - Deep analysis of code structure and quality

---

## ✨ Features

### 💬 AI Chat Assistant
- Ask any coding question
- Get clear, educational explanations
- Conversation history saved automatically
- Powered by GPT-4o-mini

### 🔍 Code Analysis
- Support for Python & JavaScript
- AI explains what your code does
- Run code safely in sandbox
- See output and errors
- 
### 🔐 Built-in Security
- Secure password hashing
- Session management
- Code runs in safe sandbox (5 sec timeout)
- No dangerous operations allowed

---

## 🏗️ Architecture

### Simple Overview

```
┌─────────────────────────────────────────────────┐
│              🌐 Frontend (Browser)               │
│                                                  │
│  Landing Page → Login/Signup → Dashboard        │
│       ↓             ↓              ↓             │
│    Home         Auth Pages    Chat/Analyze      │
└─────────────────────┬───────────────────────────┘
                      │
                      │ HTTP Requests
                      ↓
┌─────────────────────────────────────────────────┐
│           ⚙️ Flask Backend (Python)             │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │   Auth   │  │   Chat   │  │ Analyze  │     │
│  │  Module  │  │  Module  │  │  Module  │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
│       │             │             │             │
│       └─────────────┼─────────────┘             │
│                     ↓                            │
│  ┌─────────────────────────────────────────┐   │
│  │         Core Services                    │   │
│  │  • Database (SQLite)                     │   │
│  │  • OpenAI Integration                    │   │
│  │  • Code Sandbox                          │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### Component Details

```
📁 Project Structure
│
├── 🌐 Frontend
│   ├── index.html        → Landing page
│   ├── login.html        → Login page
│   ├── signup.html       → Registration
│   ├── dashboard.html    → Main hub
│   ├── chat.html         → AI chat interface
│   ├── analyze.html      → Code analyzer
│
├── ⚙️ Backend
│   ├── app.py            → Main server & routing
│   ├── auth.py           → Login/signup logic
│   ├── chat.py           → Chat with AI
│   ├── analyze.py        → Code analysis
│   ├── db.py             → Database operations
│   ├── llm.py            → OpenAI integration
│   └── sandbox.py        → Safe code execution
│
└── 💾 Database
    └── app.db            → SQLite (users & chats)
```

### How It Works

#### 1. User Authentication
```
User enters email/password
         ↓
    auth.py verifies
         ↓
    db.py checks database
         ↓
   Create session & redirect to dashboard
```

#### 2. AI Chat
```
User types question
         ↓
    chat.py receives
         ↓
    llm.py → OpenAI API
         ↓
    Get AI response
         ↓
    Save to database & show user
```

#### 3. Code Analysis
```
User pastes code
         ↓
    analyze.py processes
         ↓
    ┌─────────┴─────────┐
    ↓                   ↓
llm.py            sandbox.py
(explain)         (execute)
    ↓                   ↓
    └─────────┬─────────┘
              ↓
    Show explanation + output
```

---

## 🚀 Quick Start

### What You Need
- 🐍 Python 3.8+
- 🔑 OpenAI API key

### Installation (3 Steps)

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Set your API key**
```bash
cd backend
echo "OPENAI_API_KEY=your_key_here" > .env
```

**3. Run the server**
```bash
python app.py
```

**4. Open browser**
```
http://localhost:5000
```

🎉 **Done!**

---

## 📖 How to Use

### First Time?
1. Go to homepage
2. Click "Sign Up"
3. Enter email & password
4. Log in
5. Start using!

### Using AI Chat
1. Click "AI Chat" from dashboard
2. Type your question
3. Get instant answer
4. All conversations saved

**Example:** 
```
You: "What is a variable in Python?"
AI: "A variable is a container that stores..."
```

### Using Code Analyzer
1. Click "Code Analysis"
2. Choose language (Python/JavaScript)
3. Paste your code
4. Click "Analyze & Run"
5. See explanation + output

**Example:**
```python
# Your code
print("Hello World")

# You get:
• Explanation: "This prints text to console..."
• Output: Hello World
```

### Using Forensic Tool
1. Click "Forensic Analysis"
2. Upload file OR paste code
3. Click "Trace Code"
4. Get detailed report

---

## 🛠️ What's Inside

### Database
Two simple tables:
```
users          → id, email, password
chat_history   → id, user_id, message, response, timestamp
```
```

## 🔐 Security Features

✅ Passwords are hashed (never stored as plain text)  
✅ Code runs in isolated sandbox  
✅ 5-second timeout prevents infinite loops  
✅ Dangerous operations blocked (no file access, no system calls)  
✅ Secure session management  

---<div align="center">

**Built with ❤️ for learning to code**

🔍 **TracePoint AI** - Making code analysis simple

**Version 2.0** | February 2026

</div>
