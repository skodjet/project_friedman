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
    
        


if __name__ == "__main__":

    # Load the data from roadmap_db.csv
    from load_data import load_data
    load_data()

    # Run the app
    app.run(debug=True)
