# Entry point

from flask import Flask, Response, jsonify, render_template, redirect, request, session, url_for
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timezone
import psycopg2
import boto3
import os
from dotenv import load_dotenv
from signup_login import hash_pwd, check_pwd


app = Flask(__name__)
Scss(app)

load_dotenv()
username = os.getenv("AWS_RDS_USERNAME")
password = os.getenv("AWS_RDS_PASSWORD")
port = os.getenv("AWS_RDS_PORT")
host = os.getenv("AWS_RDS_HOSTNAME")
name = "postgres"
DATABASE_URI = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{name}"

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Configure session
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Data class for each roadmap entry. Entity
class RoadmapEntry(db.Model):
    __tablename__ = "roadmap_entry"

    external_title = db.Column(db.String(255))
    internal_title = db.Column(db.String(255))
    uploader = db.Column(db.String(255))
    length = db.Column(db.Integer)
    url = db.Column(db.String(255))
    category = db.Column(db.String(20))
    lesson_id = db.Column(db.Integer, primary_key=True, unique=True)

    # See who completed this lesson
    completed_by_users = db.relationship('UserCompleted', backref='lesson')

    def __repr__(self):
        return f"Internal title: self.internal_title"
    

# Data class for user. Entity
class User(db.Model):
    __tablename__ = "users" # To prevent Postgres conflicts
    
    email = db.Column(db.String(255), primary_key = True, unique=True, nullable=False)
    hashed_password = db.Column(db.LargeBinary(), unique=True, nullable=False)
    
    # See which lessons this user has completed
    completed_lessons = db.relationship('UserCompleted', backref='user')

    def __repr__(self):
        return f"User: {self.email}"


# Which lessons the user completed. Relationship
class UserCompleted(db.Model):
    __tablename__ = "user_lessons"
    user_email = db.Column(db.String(255), db.ForeignKey('users.email'), primary_key = True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('roadmap_entry.lesson_id'),primary_key = True)


# Context manager
with app.app_context():
    db.create_all()


# Roadmap page (homepage)
@app.route("/", methods=["POST", "GET"])
def index():

    # If the user is logged in, get the lesson IDs for the user's completed lessons
    user_email = session.get("user_email")
    completed_lessons = []
    profile_hidden = "hidden"

    if user_email:
        db_user = db.session.query(User).filter_by(email=user_email).first()
        completed_lessons = [entry.lesson_id for entry in db_user.completed_lessons]
        profile_hidden = ""

    # Helper to query csv. cat = string of category
    def get_rows(cat):
        return RoadmapEntry.query.filter_by(category = cat).all()

    # Display default modules
    if request.method == "GET":
        # Beginners Start Here
        bsh_modules = get_rows("bsh")
        # Basic Chords
        bc_modules = get_rows("basic-chords")
        # Picking 1
        pck1_modules = get_rows("picking1")
        # Articulation
        artc_modules = get_rows("artc")
        # Advanced Picking
        pck2_modules = get_rows("picking2")

        return render_template('index.html', completed_lessons = completed_lessons, 
                                             profile_hidden = profile_hidden, 
                                             bsh_modules = bsh_modules, num_bsh_modules = len(bsh_modules), 
                                             bc_modules = bc_modules, num_bc_modules = len(bc_modules), 
                                             pck1_modules = pck1_modules, num_pck1_modules = len(pck1_modules), 
                                             artc_modules = artc_modules, num_artc_modules = len(artc_modules), 
                                             pck2_modules = pck2_modules, num_pck2_modules = len(pck2_modules))
    
        
# Signup page
@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    
    # User signup
    if request.method == "POST":
        # TEST
        users = db.session.query(User).all()
        for usr in users:
            print(usr)

        user_email = request.form["email"]
        user_hashed_password = hash_pwd(request.form["password"])

        # Check if the user already exists in DB
        db_user = db.session.query(User).filter_by(email=user_email).first()

        if db_user:
            return render_template("signup.html", error="Email already in use")

        # Store user in DB
        new_user = User(
            email = user_email,
            hashed_password = user_hashed_password
        )

        db.session.add(new_user)
        db.session.commit()


        # Test
        print(f"New user - Email: {new_user.email} Hashed Password: {new_user.hashed_password}")

        return "User has signed up"
    

# Login
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    # User login. Check if login is valid
    elif request.method == "POST":
        user_email = request.form["email"]
        db_user = db.session.query(User).filter_by(email=user_email).first()
        # Email does not exist
        if not db_user:
            return render_template("login.html", 
                                   error="Invalid Email")

        pwd_correct = check_pwd(request.form["password"], db_user.hashed_password)
        # Incorrect password
        if not pwd_correct:
            return render_template("login.html", error="Invalid Password")
                        
        # Email and password both correct, redirect to roadmap with user's completed lessons checked
        # Save user's email for this session
        session["user_email"] = db_user.email
        return redirect(url_for('index'))
    

# Update user data after completing a lesson
@app.route("/update-progress", methods=["POST"]) 
def update_progress() -> Response:
    user_email = session.get("user_email")

    # Return 401 if user isn't logged in and somehow POSTed to here
    if not user_email:
        return jsonify({"error": "Unauthorized"}), 401

    # Get the data sent from fetch() in JS
    data = request.get_json()
    lesson_id = data['lesson_id']
    status = data['status']

    # TEST
    print(f"lesson_id: {lesson_id}")
    print(f"status: {status}")

    # Push the update to RDS
    # Add a record
    if status == "True":
        new_entry = UserCompleted(user_email = user_email, lesson_id = lesson_id)
        try:
            db.session.add(new_entry)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {e}")
            return jsonify({"error": str(e)}), 500

    # Delete a record
    else:
        try:
            record = db.session.query(UserCompleted).filter_by(user_email = user_email, lesson_id = lesson_id).first()
            if record:
                db.session.delete(record)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {e}")
            return jsonify({"error": str(e)}), 500
        
    return jsonify({"status": "success"}), 200
    
        
        

if __name__ == "__main__":
    from signup_login import hash_pwd, check_pwd
    # Load the data from roadmap_db.csv
    from load_data import load_data
    load_data()

    # Run the app
    app.run(debug=True)
