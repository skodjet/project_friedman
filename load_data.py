import csv
from app import db, RoadmapEntry, app


def load_data():
    with app.app_context():
        with open("roadmap_db.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                entry = RoadmapEntry(
                    external_title = row["external_title"], 
                    internal_title = row["internal_title"], 
                    uploader = row["uploader"], 
                    length = row["length"], 
                    url = row["url"], 
                    category = row["category"], 
                    ordering = row["ordering"]
                )
                db.session.add(entry)

            db.session.commit()