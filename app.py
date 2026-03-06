from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/")
def root():
    return {"status": "API działa"}

def get_db():
    return sqlite3.connect("attendance.db")


# ---------- PRESENCE ----------

@app.post("/log")
def add_log(name: str, termin: str, czas: str):

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS log (name TEXT, termin TEXT, czas TEXT)"
    )

    # zapobiega duplikatom
    cur.execute(
        "SELECT * FROM log WHERE name=? AND termin=?",
        (name, termin)
    )

    if not cur.fetchone():
        cur.execute(
            "INSERT INTO log VALUES (?, ?, ?)",
            (name, termin, czas)
        )

    db.commit()

    return {"status": "ok"}


@app.get("/log")
def get_log():

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS log (name TEXT, termin TEXT, czas TEXT)"
    )

    cur.execute("SELECT * FROM log")

    rows = cur.fetchall()

    return rows


# ---------- NOTES ----------

@app.post("/note")
def add_note(name: str, note: str):

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS notes (name TEXT PRIMARY KEY, note TEXT)"
    )

    cur.execute(
        "INSERT OR REPLACE INTO notes VALUES (?, ?)",
        (name, note)
    )

    db.commit()

    return {"status": "ok"}

@app.post("/delete")
def delete_log(name: str, termin: str):

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "DELETE FROM log WHERE name=? AND termin=?",
        (name, termin)
    )

    db.commit()

    return {"status": "deleted"}


@app.get("/notes")
def get_notes():

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS notes (name TEXT PRIMARY KEY, note TEXT)"
    )

    cur.execute("SELECT * FROM notes")

    rows = cur.fetchall()

    return [{"name": r[0], "note": r[1]} for r in rows]
