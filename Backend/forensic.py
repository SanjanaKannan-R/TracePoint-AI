"""
TracePoint AI - Enhanced Forensic Analysis Module
Comprehensive code forensics with AI
"""

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from llm import forensic_analysis
from werkzeug.utils import secure_filename
import os

forensic = Blueprint("forensic", __name__)

ALLOWED_EXTENSIONS = {
    'txt', 'py', 'js', 'java', 'cpp', 'c', 'h', 'hpp',
    'html', 'css', 'json', 'xml', 'yml', 'yaml',
    'php', 'rb', 'go', 'rs', 'swift', 'kt', 'ts', 'jsx', 'tsx'
}

MAX_FILE_SIZE = 1024 * 1024  # 1MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_extension(filename):
    """Get file extension"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''


@forensic.route("/forensic", methods=["GET", "POST"])
@login_required
def forensic_page():
    """
    Main forensic analysis page and handler
    """
    if request.method == "GET":
        return render_template("forensic.html")
    
    try:
        answer = None
        
        # Handle question about forensic analysis
        if request.form.get("question"):
            question = request.form.get("question", "").strip()
            if question:
                print(f"❓ Forensic question: {question[:50]}...")
                
                # Use forensic-specific AI response
                from llm import chat_response
                answer = chat_response(
                    f"As a code forensics expert, answer this: {question}",
                    "developer"
                )
        
        # Handle file upload
        elif 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            
            if not allowed_file(file.filename):
                answer = f"❌ File type not supported: {get_file_extension(file.filename)}\n\nSupported types: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            else:
                filename = secure_filename(file.filename)
                print(f"📁 Analyzing uploaded file: {filename}")
                
                try:
                    content = file.read()
                    
                    # Check file size
                    if len(content) > MAX_FILE_SIZE:
                        answer = f"❌ File too large: {len(content)/1024:.1f}KB\n\nMaximum size: {MAX_FILE_SIZE/1024:.0f}KB"
                    else:
                        # Decode file content
                        try:
                            code_text = content.decode('utf-8')
                        except UnicodeDecodeError:
                            try:
                                code_text = content.decode('latin-1')
                            except:
                                answer = "❌ Unable to decode file. Please ensure it's a text file with UTF-8 or Latin-1 encoding."
                                code_text = None
                        
                        if code_text:
                            print(f"🔍 Running forensic analysis on {filename} ({len(code_text)} chars)...")
                            answer = forensic_analysis(code_text, filename)
                            print(f"✅ Forensic analysis complete")
                
                except Exception as e:
                    answer = f"❌ Error processing file: {str(e)}"
        
        # Handle pasted code
        elif request.form.get("code_text"):
            code_text = request.form.get("code_text", "").strip()
            
            if not code_text:
                answer = "⚠️ No code provided"
            elif len(code_text) > 100000:  # 100KB limit for pasted code
                answer = f"❌ Code too long: {len(code_text)} characters\n\nMaximum: 100,000 characters"
            else:
                print(f"🔍 Running forensic analysis on pasted code ({len(code_text)} chars)...")
                answer = forensic_analysis(code_text)
                print(f"✅ Forensic analysis complete")
        
        else:
            answer = "⚠️ No input provided. Please upload a file, paste code, or ask a question."
        
        return render_template("forensic.html", answer=answer)
    
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Forensic analysis error: {error_msg}")
        return render_template("forensic.html", answer=f"❌ Analysis failed: {error_msg}")


@forensic.route("/forensic/api", methods=["POST"])
@login_required
def forensic_api():
    """
    API endpoint for programmatic forensic analysis
    """
    try:
        data = request.get_json()
        if not data or "code" not in data:
            return jsonify({"error": "No code provided"}), 400
        
        code = data["code"]
        filename = data.get("filename")
        analysis_type = data.get("type", "comprehensive").lower()
        
        if len(code) > 100000:
            return jsonify({"error": "Code too long (max 100KB)"}), 400
        
        # Different analysis types for API users
        if analysis_type == "security":
            from llm import ask_llm, get_enhanced_system_prompt
            
            system = """You are a security analyst. Focus exclusively on:
1. Security vulnerabilities (SQL injection, XSS, CSRF, etc.)
2. Unsafe operations (eval, exec, system calls)
3. Authentication and authorization issues
4. Data exposure risks
5. Cryptography weaknesses

Provide a prioritized list of security findings."""
            
            result = ask_llm(system, f"Analyze this code for security issues:\n\n{code}")
        
        elif analysis_type == "quality":
            from llm import ask_llm
            
            system = """You are a code quality expert. Focus on:
1. Code readability and clarity
2. Design patterns and architecture
3. Code smells and anti-patterns
4. Best practices compliance
5. Maintainability issues

Provide specific, actionable recommendations."""
            
            result = ask_llm(system, f"Analyze this code for quality:\n\n{code}")
        
        elif analysis_type == "performance":
            from llm import ask_llm
            
            system = """You are a performance optimization expert. Focus on:
1. Algorithm complexity (Big-O analysis)
2. Inefficient operations
3. Resource usage (memory, CPU)
4. Database query optimization
5. Caching opportunities

Provide specific optimization suggestions."""
            
            result = ask_llm(system, f"Analyze this code for performance:\n\n{code}")
        
        else:  # comprehensive (default)
            result = forensic_analysis(code, filename)
        
        return jsonify({
            "analysis": result,
            "type": analysis_type,
            "code_length": len(code),
            "filename": filename
        }), 200
    
    except Exception as e:
        error_msg = str(e)
        print(f"❌ API forensic error: {error_msg}")
        return jsonify({
            "error": "Analysis failed",
            "details": error_msg
        }), 500


@forensic.route("/forensic/batch", methods=["POST"])
@login_required
def batch_analysis():
    """
    Analyze multiple code files in batch
    """
    try:
        data = request.get_json()
        if not data or "files" not in data:
            return jsonify({"error": "No files provided"}), 400
        
        files = data["files"]
        if not isinstance(files, list):
            return jsonify({"error": "Files must be an array"}), 400
        
        if len(files) > 10:
            return jsonify({"error": "Maximum 10 files per batch"}), 400
        
        results = []
        
        for file_data in files:
            if "code" not in file_data:
                results.append({"error": "Missing code", "filename": file_data.get("filename", "unknown")})
                continue
            
            code = file_data["code"]
            filename = file_data.get("filename", "unnamed")
            
            if len(code) > 50000:
                results.append({
                    "error": "File too large",
                    "filename": filename,
                    "size": len(code)
                })
                continue
            
            try:
                analysis = forensic_analysis(code, filename)
                results.append({
                    "filename": filename,
                    "analysis": analysis,
                    "success": True
                })
            except Exception as e:
                results.append({
                    "filename": filename,
                    "error": str(e),
                    "success": False
                })
        
        return jsonify({
            "results": results,
            "total": len(files),
            "successful": sum(1 for r in results if r.get("success", False))
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Batch analysis failed",
            "details": str(e)
        }), 500