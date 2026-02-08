"""
TracePoint AI - Main Application
Production-ready Flask app without forensic features
"""

from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, login_required, current_user
from flask_cors import CORS
from auth import auth, User
from analyze import analyze
from chat import chat
from db import init_db, get_conn
import os
import sys

# Configuration
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, "Frontend", "templates")
STATIC_FOLDER = os.path.join(BASE_DIR, "Frontend", "static")

# Try alternative paths if standard structure doesn't exist
if not os.path.exists(TEMPLATE_FOLDER):
    TEMPLATE_FOLDER = os.path.join(os.path.dirname(__file__), "templates")
if not os.path.exists(STATIC_FOLDER):
    STATIC_FOLDER = os.path.join(os.path.dirname(__file__), "static")

# Create Flask app
app = Flask(
    __name__,
    template_folder=TEMPLATE_FOLDER,
    static_folder=STATIC_FOLDER,
)

# Security configuration
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "tracepoint-secure-key-2026-change-in-production")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB max upload
app.config["SESSION_COOKIE_SECURE"] = False  # Set True in production with HTTPS
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Enable CORS
CORS(app, resources={
    r"/api/*": {"origins": "*"},
    r"/analyze": {"origins": "*"},
    r"/chat": {"origins": "*"}
})

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """Load user from database"""
    try:
        with get_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE id=?", (user_id,))
            row = c.fetchone()
            return User(row) if row else None
    except Exception as e:
        print(f"❌ Error loading user: {e}")
        return None

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(analyze)
app.register_blueprint(chat)

# Routes
@app.route("/")
def index():
    """Landing page"""
    return render_template("index.html")

@app.route("/dashboard")
@login_required
def dashboard():
    """User dashboard - requires login"""
    return render_template("dashboard.html", user=current_user)

@app.route("/health")
def health():
    """Health check endpoint"""
    try:
        import llm
        api_status, api_message = llm.test_llm_connection()
    except Exception as e:
        api_status = False
        api_message = f"LLM module error: {str(e)}"
    
    return jsonify({
        "status": "online",
        "version": "2.0-Production",
        "app": "TracePoint AI",
        "api_configured": api_status,
        "api_status": api_message,
        "features": {
            "code_analysis": True,
            "chat": True,
            "sandbox": True
        }
    }), 200

@app.route("/api/status")
def api_status():
    """Detailed API status"""
    try:
        import llm
        api_ok, api_msg = llm.test_llm_connection()
    except Exception as e:
        api_ok = False
        api_msg = f"LLM import error: {str(e)}"
    
    return jsonify({
        "server": {
            "status": "running",
            "python_version": sys.version,
            "flask_debug": app.debug
        },
        "openai_api": {
            "configured": api_ok,
            "status": api_msg
        },
        "database": {
            "status": "connected",
            "path": "app.db"
        }
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(e):
    """404 error handler"""
    if request.path.startswith('/api/'):
        return jsonify({"error": "Endpoint not found"}), 404
    return render_template("404.html") if os.path.exists(os.path.join(TEMPLATE_FOLDER, "404.html")) else jsonify({"error": "Page not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    """500 error handler"""
    print(f"❌ Internal error: {e}")
    if request.path.startswith('/api/'):
        return jsonify({"error": "Internal server error"}), 500
    return jsonify({"error": "Internal server error. Please try again."}), 500

@app.errorhandler(413)
def request_entity_too_large(e):
    """413 error handler - file too large"""
    return jsonify({"error": "File too large. Maximum size is 10MB."}), 413

@app.before_request
def log_request():
    """Log all requests in debug mode"""
    if app.debug:
        print(f"📥 {request.method} {request.path}")

@app.after_request
def after_request(response):
    """Add security headers"""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

def initialize_app():
    """Initialize application components"""
    print("\n" + "="*70)
    print("🚀 TRACEPOINT AI - STARTING")
    print("="*70)
    
    # Initialize database
    print("\n📊 Initializing database...")
    try:
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False
    
    # Create directories
    print("\n📁 Creating directories...")
    try:
        os.makedirs(STATIC_FOLDER, exist_ok=True)
        os.makedirs(TEMPLATE_FOLDER, exist_ok=True)
        print(f"✅ Static folder: {STATIC_FOLDER}")
        print(f"✅ Template folder: {TEMPLATE_FOLDER}")
    except Exception as e:
        print(f"❌ Directory creation failed: {e}")
        return False
    
    # Test LLM connection
    print("\n🤖 Testing LLM connection...")
    try:
        import llm
        api_ok, api_msg = llm.test_llm_connection()
        print(api_msg)
        
        if not api_ok:
            print("\n⚠️  WARNING: OpenAI API not configured!")
            print("   The app will run with limited functionality.")
            print("   To enable AI features:")
            print("   1. Get API key from: https://platform.openai.com/api-keys")
            print("   2. Set: export OPENAI_API_KEY='your-key-here'")
            print("   3. Restart the application")
    except ImportError as e:
        print(f"❌ Failed to import llm module: {e}")
        print("   Make sure llm.py is in the same directory as app.py")
        return False
    except Exception as e:
        print(f"⚠️  LLM test failed: {e}")
        print("   The app will start but AI features may not work")
    
    print("\n" + "="*70)
    print("✅ SERVER READY")
    print("="*70)
    print(f"\n🌐 Main: http://localhost:5000")
    print(f"📊 Dashboard: http://localhost:5000/dashboard")
    print(f"🔬 Analyze: http://localhost:5000/analyze/page")
    print(f"💬 Chat: http://localhost:5000/chat/page")
    print(f"🏥 Health: http://localhost:5000/health")
    print("="*70 + "\n")
    
    return True

if __name__ == "__main__":
    if initialize_app():
        # Run server
        app.run(
            debug=True,
            host="0.0.0.0",
            port=5000,
            threaded=True
        )
    else:
        print("\n❌ Initialization failed. Cannot start server.")