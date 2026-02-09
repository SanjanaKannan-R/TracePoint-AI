from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, UserMixin, current_user
from db import create_user, get_user_by_email, verify_user

auth = Blueprint("auth", __name__)

class User(UserMixin):
    def __init__(self, row):
        self.id = row[0]
        self.username = row[1]
        self.email = row[2]
    
    def get_id(self):
        return str(self.id)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        
        if not username or not email or not password:
            flash("Username, email and password are required", "error")
            return render_template("signup.html")
        
        if len(username) < 3:
            flash("Username must be at least 3 characters", "error")
            return render_template("signup.html")
        
        if len(password) < 6:
            flash("Password must be at least 6 characters", "error")
            return render_template("signup.html")
        
        try:
            create_user(username, email, password)
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("auth.login"))
        except ValueError as e:
            flash(str(e), "error")
        except Exception as e:
            flash("Registration failed. Please try again.", "error")
    
    return render_template("signup.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        
        if not email or not password:
            flash("Email and password are required", "error")
            return render_template("login.html")
        
        user_row = verify_user(email, password)
        if user_row:
            user = User(user_row)
            login_user(user, remember=True)
            
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("dashboard"))
        
        flash("Invalid email or password", "error")
    
    return render_template("login.html")

@auth.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out", "success")
    return redirect(url_for("index"))
