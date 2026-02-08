"""
TracePoint AI - PRO Gemini Edition
Integrated with Google Gemini 2.0 Flash for real-world AI reasoning.
"""

import os
from google import genai
from google.genai import types
from datetime import datetime

# Initialize Gemini Client
# Ensure you have set GEMINI_API_KEY in your environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# ==================== SYSTEM PROMPTS ====================
# Explicitly telling the AI its role to improve accuracy
SYSTEM_PROMPTS = {
    "beginner": "You are a patient, friendly coding teacher for beginners. Explain concepts using analogies and avoid complex jargon unless you define it first.",
    "developer": "You are a senior software engineer and code reviewer. Focus on best practices, design patterns, optimization, and maintainability.",
    "researcher": "You are a computer science researcher. Focus on algorithmic complexity (Big O), theoretical foundations, and formal verification.",
    "forensics": "You are a cybersecurity forensic expert. Deep-scan code for vulnerabilities, data leaks, and malicious logic. Provide a formal security audit."
}

def analyze_code_with_ai(code, lang, audience="beginner"):
    """
    Performs high-level code analysis using Gemini.
    """
    try:
        role_prompt = SYSTEM_PROMPTS.get(audience, SYSTEM_PROMPTS["beginner"])
        full_prompt = f"{role_prompt}\n\nAnalyze this {lang} code and provide a detailed explanation:\n\n{code}"
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=full_prompt
        )
        return response.text
    except Exception as e:
        return f"⚠️ AI Analysis Error: {str(e)}"

def chat_response(message, audience="beginner", history=None):
    """
    Handles conversational chat with context/history.
    'history' should be a list of dicts: [{'role': 'user', 'parts': [...]}, ...]
    """
    try:
        role_prompt = SYSTEM_PROMPTS.get(audience, SYSTEM_PROMPTS["beginner"])
        
        # Initialize chat with system instruction
        chat = client.chats.create(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(system_instruction=role_prompt),
            history=history or []
        )
        
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        return f"⚠️ Chat Error: {str(e)}"

def answer_code_question(question, code, lang, audience="beginner"):
    """
    Answers a specific question about a provided block of code.
    """
    try:
        role_prompt = SYSTEM_PROMPTS.get(audience, SYSTEM_PROMPTS["beginner"])
        context_prompt = f"Code Context ({lang}):\n```\n{code}\n```\n\nQuestion: {question}"
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(system_instruction=role_prompt),
            contents=context_prompt
        )
        return response.text
    except Exception as e:
        return f"⚠️ Q&A Error: {str(e)}"

def forensic_analysis(code, filename=None):
    """
    Generates a professional forensic security report.
    """
    try:
        report_template = (
            "Generate a formal Forensic Code Analysis Report. "
            "Include sections for: 1. Executive Summary, 2. Structural Analysis, "
            "3. Security Vulnerabilities (High/Med/Low), 4. Data Flow Integrity, and 5. Remediation Steps."
        )
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPTS["forensics"]),
            contents=f"{report_template}\n\nFile: {filename or 'Input'}\n\nCode:\n{code}"
        )
        return response.text
    except Exception as e:
        return f"⚠️ Forensic Engine Error: {str(e)}"