import json
import re
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://flaskuser:flaskpass@localhost/flask_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Record(db.Model):
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(49), nullable=False)
    date = db.Column(db.DateTime, nullable=False)


DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}:\d{2}$")


def validate_and_parse(data):
    if not isinstance(data, list):
        return None, "JSON must be str"

    records = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            return None, "should be object"

        if "name" not in item:
            return None, "no name key"
        if "date" not in item:
            return None, "no date key"

        name = item["name"]
        date_str = item["date"]

        if not isinstance(name, str) or len(name) >= 50:
            return None, "need less 50"

        if not isinstance(date_str, str) or not DATE_PATTERN.match(date_str):
            return None, "data error"

        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d_%H:%M")
        except ValueError:
            return None, "not ivalid date"

        records.append({"name": name, "date": parsed_date})

    return records, None


@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("json_file")

        if not file or file.filename == "":
            flash("No file", "danger")
            return redirect(url_for("upload"))

        if not file.filename.endswith(".json"):
            flash(".json files only", "danger")
            return redirect(url_for("upload"))

        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            flash(f"JSON error: {e}", "danger")
            return redirect(url_for("upload"))

        records, error = validate_and_parse(data)
        if error:
            flash(f"Error: {error}", "danger")
            return redirect(url_for("upload"))

        for r in records:
            db.session.add(Record(name=r["name"], date=r["date"]))
        db.session.commit()

        flash(f"Loaded {len(records)} records!", "success")
        return redirect(url_for("records"))

    return render_template("upload.html")


@app.route("/records")
def records():
    all_records = Record.query.order_by(Record.id.desc()).all()
    return render_template("records.html", records=all_records)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
