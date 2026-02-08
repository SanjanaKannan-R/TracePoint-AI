import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with all required tables"""
    with get_conn() as conn:
        c = conn.cursor()
        
        # Users table
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Chat history table
        c.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        
        # Create indexes for better performance
        c.execute("""
        CREATE INDEX IF NOT EXISTS idx_chat_user_id 
        ON chat_history(user_id)
        """)
        
        c.execute("""
        CREATE INDEX IF NOT EXISTS idx_chat_timestamp 
        ON chat_history(timestamp)
        """)
        
        conn.commit()
    print("Database initialized successfully")

# ==================== USER AUTH ====================

def create_user(email, password):
    """Create a new user account"""
    if not email or not password:
        raise ValueError("Email and password are required")
    
    with get_conn() as conn:
        c = conn.cursor()
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        try:
            c.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email.lower(), hashed_password)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            raise ValueError("User with this email already exists")

def get_user_by_email(email):
    """Retrieve user by email"""
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=?", (email.lower(),))
        return c.fetchone()

def get_user_by_id(user_id):
    """Retrieve user by ID"""
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id=?", (user_id,))
        return c.fetchone()

def verify_user(email, password):
    """Verify user credentials"""
    user = get_user_by_email(email)
    if user and check_password_hash(user[2], password):
        return user
    return None

# ==================== CHAT HISTORY ====================

def save_chat(user_id, message, response):
    """Save a chat exchange to history"""
    with get_conn() as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO chat_history (user_id, message, response, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, message, response, datetime.utcnow().isoformat())
        )
        conn.commit()

def get_history(user_id, limit=50):
    """Get chat history for a user"""
    with get_conn() as conn:
        c = conn.cursor()
        c.execute(
            """SELECT message, response, timestamp 
               FROM chat_history 
               WHERE user_id=? 
               ORDER BY id DESC 
               LIMIT ?""",
            (user_id, limit)
        )
        return c.fetchall()

def delete_user_history(user_id):
    """Delete all chat history for a user"""
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM chat_history WHERE user_id=?", (user_id,))
        conn.commit()

def get_chat_count(user_id):
    """Get total number of chats for a user"""
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM chat_history WHERE user_id=?", (user_id,))
        return c.fetchone()[0]