from contextlib import closing
from datetime import date
from pathlib import Path
import sqlite3

from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)
DATABASE = Path(__file__).resolve().parent / "data" / "events.db"


def connect_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    DATABASE.parent.mkdir(exist_ok=True)
    with closing(connect_db()) as db, db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)


def event_form():
    event = {field: request.form.get(field, "").strip()
             for field in ("name", "date", "description")}
    if not all(event.values()):
        return event, "Please fill in all fields."
    try:
        event["date"] = date.fromisoformat(event["date"]).isoformat()
    except ValueError:
        return event, "Please enter a valid event date."
    return event, None


def show_events(event=None, error=None):
    with closing(connect_db()) as db:
        events = db.execute("SELECT * FROM events ORDER BY date, id").fetchall()
    return render_template("index.html", events=events, event=event or {}, error=error)


@app.get("/")
def index():
    return show_events()


@app.post("/add")
def add():
    event, error = event_form()
    if error:
        return show_events(event, error), 400
    with closing(connect_db()) as db, db:
        db.execute("INSERT INTO events (name, date, description) VALUES (:name, :date, :description)", event)
    return redirect(url_for("index"))


@app.route("/edit/<int:event_id>", methods=["GET", "POST"])
def edit(event_id):
    with closing(connect_db()) as db, db:
        event = db.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
        if event is None:
            abort(404)
        if request.method == "POST":
            event, error = event_form()
            if error:
                return render_template("edit.html", event=event, error=error), 400
            result = db.execute(
                "UPDATE events SET name = :name, date = :date, description = :description WHERE id = :id",
                {**event, "id": event_id},
            )
            if not result.rowcount:
                abort(404)
            return redirect(url_for("index"))
    return render_template("edit.html", event=event)


@app.post("/delete/<int:event_id>")
def delete(event_id):
    with closing(connect_db()) as db, db:
        result = db.execute("DELETE FROM events WHERE id = ?", (event_id,))
        if not result.rowcount:
            abort(404)
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
