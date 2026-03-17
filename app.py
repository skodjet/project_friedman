# Entry point

from flask import Flask, render_template, redirect, request
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

# Data class for each roadmap entry
class RoadmapEntry(db.Model):
    external_title = db.Column(db.String(255))
    internal_title = db.Column(db.String(255))
    uploader = db.Column(db.String(255))
    length = db.Column(db.Integer)
    url = db.Column(db.String(255), primary_key=True)
    category = db.Column(db.String(20))
    ordering = db.Column(db.Integer)

    def __repr__(self):
        return f"Internal title: self.internal_title"
    

# Data class for user
class User(db.Model):
    __tablename__ = "users" # To prevent Postgres conflicts
    
    email = db.Column(db.String(255), primary_key = True, unique=True, nullable=False)
    hashed_password = db.Column(db.LargeBinary(), unique=True, nullable=False)

    def __repr__(self):
        return f"User: {self.email}"
    

# Context manager
with app.app_context():
    db.create_all()


# Roadmap page (homepage)
@app.route("/", methods=["POST", "GET"])
def index():

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

        return render_template('index.html', bsh_modules = bsh_modules, num_bsh_modules = len(bsh_modules), 
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
        user_email = request.form["email"]
        user_hashed_password = hash_pwd(request.form["password"])

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
        user_hashed_password = hash_pwd(request.form["password"])
        db_user = db.session.query(User.email).filter_by(email=user_email).first()
        # Email does not exist
        if not db_user:
            return render_template("login.html", 
                                   error="Invalid Email")
                



if __name__ == "__main__":
    from signup_login import hash_pwd, check_pwd
    # Load the data from roadmap_db.csv
    from load_data import load_data
    load_data()

    # Run the app
    app.run(debug=True)
