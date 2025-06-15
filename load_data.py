import csv
from app import db, RoadmapEntry, app


def load_data():
    with app.app_context():

        # Delete all previous data
        RoadmapEntry.__table__.drop(db.engine)
        db.create_all()
        
        with open("roadmap_db.csv", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            # DEBUG
            # existing_urls = {row.url for row in RoadmapEntry.query.all()}
            # print(existing_urls)
            # exit(1)

            for row in reader:

                # DEBUG
                # print("\nURL: " + row["url"])

                entry = RoadmapEntry(
                    external_title = row["external_title"], 
                    internal_title = row["internal_title"], 
                    uploader = row["uploader"], 
                    length = row["length"], 
                    url = row["url"].strip(),
                    category = row["category"], 
                    ordering = row["ordering"]
                )
                db.session.add(entry)

                # DEBUG
                # print(entry)

            db.session.commit()