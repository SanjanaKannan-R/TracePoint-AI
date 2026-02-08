from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from llm import analyze_code_with_ai

analyze = Blueprint("analyze", __name__)

@analyze.route("/analyze", methods=["POST"])
@login_required
def analyze_code():
    """Analyze code with AI - returns analysis and voice-ready text"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        code = data.get("code", "").strip()
        lang = data.get("lang", "py").strip().lower()
        
        if not code:
            return jsonify({"error": "No code provided"}), 400
        
        if len(code) > 50000:
            return jsonify({"error": "Code too long. Maximum 50,000 characters."}), 400
        
        # Supported languages
        supported_langs = ["py", "js", "java", "cpp", "c", "html", "css", "sql"]
        if lang not in supported_langs:
            return jsonify({"error": f"Unsupported language: {lang}"}), 400
        
        print(f"🔍 Analyzing {lang} code ({len(code)} chars)...")
        
        # Get AI analysis
        explanation = analyze_code_with_ai(code, lang, "beginner")
        
        # Create voice-friendly summary
        voice_text = f"Analysis complete. This is {lang.upper()} code with {len(code.split(chr(10)))} lines. {explanation[:200]}..."
        
        print(f"✅ Analysis complete")
        
        return jsonify({
            "explanation": explanation,
            "voice_text": voice_text,
            "language": lang,
            "line_count": len(code.split('\n')),
            "success": True
        }), 200
    
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Analysis error: {error_msg}")
        return jsonify({
            "error": f"Analysis failed: {error_msg}",
            "success": False
        }), 500


@analyze.route("/analyze/page")
@login_required
def analyze_page():
    """Render the code analysis page"""
    return render_template("analyze.html")