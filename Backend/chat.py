"""
TracePoint AI - Enhanced Chat Module
Better conversation handling and AI integration
"""

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from llm import chat_response, answer_code_question
from db import save_chat, get_history

chat = Blueprint("chat", __name__)

@chat.route("/chat", methods=["POST"])
@login_required
def chat_api():
    """
    Main chat endpoint - handles general programming questions
    Enhanced with better context and responses
    """
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "No message provided"}), 400
        
        msg = data["message"].strip()
        if not msg:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        if len(msg) > 5000:
            return jsonify({"error": "Message too long. Maximum 5000 characters."}), 400
        
        # Get audience level from request or default to beginner
        audience = data.get("audience", "beginner").strip().lower()
        if audience not in ["beginner", "developer", "researcher"]:
            audience = "beginner"
        
        print(f"💬 Chat request from user {current_user.id}: {msg[:50]}...")
        
        # Generate response
        reply = chat_response(msg, audience)
        
        # Save to history
        save_chat(current_user.id, msg, reply)
        
        print(f"✅ Chat response generated ({len(reply)} chars)")
        
        return jsonify({
            "reply": reply,
            "timestamp": "now",
            "audience": audience
        }), 200
    
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Chat error: {error_msg}")
        return jsonify({
            "error": "Sorry, I encountered an error. Please try again.",
            "details": error_msg
        }), 500


@chat.route("/chat/code", methods=["POST"])
@login_required
def chat_with_code():
    """
    Chat endpoint for code-specific questions
    Allows users to ask questions about provided code
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        question = (data.get("question") or "").strip()
        code = (data.get("code") or "").strip()
        language = (data.get("language") or "py").strip().lower()
        audience = (data.get("audience") or "beginner").strip().lower()

        # Validation
        if not question:
            return jsonify({"error": "Question cannot be empty"}), 400
        
        if not code:
            return jsonify({"error": "Code context is required for code-specific questions"}), 400
        
        if len(question) > 2000:
            return jsonify({"error": "Question too long. Maximum 2000 characters."}), 400
        
        if len(code) > 50000:
            return jsonify({"error": "Code too long. Maximum 50,000 characters."}), 400
        
        # Validate audience
        if audience not in ["beginner", "developer", "researcher"]:
            audience = "beginner"
        
        print(f"💬 Code Q&A from user {current_user.id}: {question[:50]}...")
        print(f"   Code: {len(code)} chars, Language: {language}")
        
        # Get answer with code context
        answer = answer_code_question(question, code, language, audience)
        
        # Save to history
        save_chat(current_user.id, f"[Code Question] {question}", answer)
        
        print(f"✅ Code Q&A response generated")
        
        return jsonify({
            "answer": answer,
            "timestamp": "now",
            "language": language,
            "audience": audience
        }), 200
    
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Code Q&A error: {error_msg}")
        return jsonify({
            "error": "Failed to answer your question. Please try again.",
            "details": error_msg
        }), 500


@chat.route("/chat/history", methods=["GET"])
@login_required
def chat_history():
    """
    Get chat history for the current user
    """
    try:
        # Get limit from query params (default 50, max 200)
        limit = min(int(request.args.get("limit", 50)), 200)
        
        history = get_history(current_user.id, limit)
        
        formatted_history = [
            {
                "message": row[0],
                "response": row[1],
                "timestamp": row[2]
            }
            for row in history
        ]
        
        return jsonify({
            "history": formatted_history,
            "count": len(formatted_history),
            "limit": limit
        }), 200
    
    except Exception as e:
        error_msg = str(e)
        print(f"❌ History retrieval error: {error_msg}")
        return jsonify({
            "error": "Failed to retrieve chat history",
            "details": error_msg
        }), 500


@chat.route("/chat/clear", methods=["POST"])
@login_required
def clear_history():
    """
    Clear chat history for the current user
    """
    try:
        from db import delete_user_history
        delete_user_history(current_user.id)
        
        return jsonify({
            "success": True,
            "message": "Chat history cleared successfully"
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Failed to clear history",
            "details": str(e)
        }), 500


@chat.route("/chat/page")
@login_required
def chat_page():
    """Render the chat interface page"""
    return render_template("chat.html")


@chat.route("/chat/stats", methods=["GET"])
@login_required
def chat_stats():
    """
    Get chat statistics for the current user
    """
    try:
        from db import get_chat_count
        total_chats = get_chat_count(current_user.id)
        
        return jsonify({
            "total_chats": total_chats,
            "user_id": current_user.id,
            "user_email": current_user.email
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Failed to get stats",
            "details": str(e)
        }), 500