from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timezone


app = Flask(__name__)
Scss(app)

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
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
        return self.internal_title


# Context manager
with app.app_context():
    db.create_all()


# Roadmap page (homepage)
@app.route("/", methods=["POST", "GET"])
def index():
    # Display default modules
    if request.method == "GET":
        # Beginners Start Here
        bsh_modules = RoadmapEntry.query.filter_by(category = "bsh").all()
        # Basic Chords
        bc_modules = RoadmapEntry.query.filter_by(category = "basic-chords").all()

        return render_template('index.html', bsh_modules = bsh_modules, num_bsh_modules = len(bsh_modules), 
                                             bc_modules = bc_modules, num_bc_modules = len(bc_modules))
    
        


if __name__ == "__main__":

    # Load the data from roadmap_db.csv
    from load_data import load_data
    load_data()

    # Run the app
    app.run(debug=True)
