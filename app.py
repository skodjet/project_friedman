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
    length = db.Column(db.Integer)
    url = db.Column(db.String(255), primary_key=True)
    # TODO: Figure out how JSON works in SQLAlchemy and Flask
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
        # Get beginners start here modules
        bsh_modules = RoadmapEntry.query.filter_by(category = "bsh").all()


        return render_template('index.html', bsh_modules=bsh_modules)
    
    




if __name__ == "__main__":
    # Load the data from roadmap_db.csv
    from load_data import load_data
    load_data()

    # Run the app
    app.run(debug=True)
