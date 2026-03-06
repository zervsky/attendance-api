from fastapi import FastAPI
import sqlite3

app = FastAPI()

def get_db():
    return sqlite3.connect("attendance.db")

@app.get("/log")
def get_log():
    db = get_db()
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS log (name TEXT, termin TEXT, czas TEXT)")
    cur.execute("SELECT * FROM log")
    rows = cur.fetchall()
    return rows

@app.post("/log")
def add_log(name: str, termin: str, czas: str):
    db = get_db()
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS log (name TEXT, termin TEXT, czas TEXT)")
    cur.execute(
        "INSERT INTO log VALUES (?, ?, ?)",
        (name, termin, czas)
    )
    db.commit()
    return {"status": "ok"}
