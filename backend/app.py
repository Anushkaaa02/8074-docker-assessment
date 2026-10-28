import os

import psycopg
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_connection():
    return psycopg.connect(
        host=os.environ.get("DB_HOST", "db"),
        dbname=os.environ.get("DB_NAME", "festpass"),
        user=os.environ.get("DB_USER", "festpass"),
        password=os.environ.get("DB_PASSWORD", ""),
        connect_timeout=3,
    )


def ensure_registration_table(connection):
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS registrations (
            id BIGSERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            event TEXT NOT NULL,
            regno TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
        """
    )


@app.get("/health")
def health():
    return jsonify(status="ok", regno=os.environ.get("REGNO", "8074"))


@app.get("/api/health")
def database_health():
    try:
        with get_connection() as connection:
            connection.execute("SELECT 1")
    except psycopg.Error:
        return jsonify(status="unavailable", database="disconnected"), 503
    return jsonify(status="ok", database="connected")


@app.get("/api/registrations")
def list_registrations():
    try:
        with get_connection() as connection:
            ensure_registration_table(connection)
            rows = connection.execute(
                """
                SELECT id, name, event, regno, created_at
                FROM registrations
                ORDER BY created_at DESC, id DESC
                LIMIT 100
                """
            ).fetchall()
    except psycopg.Error:
        return jsonify(error="Registration service is unavailable."), 503

    return jsonify(
        registrations=[
            {
                "id": row[0],
                "name": row[1],
                "event": row[2],
                "regno": row[3],
                "created_at": row[4].isoformat(),
            }
            for row in rows
        ]
    )


@app.post("/api/registrations")
def create_registration():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Send registration details as JSON."), 400

    fields = ("name", "email", "event")
    if any(not isinstance(payload.get(field), str) for field in fields):
        return jsonify(error="Name, email, and event must be text."), 400

    name = payload["name"].strip()
    email = payload["email"].strip()
    event = payload["event"].strip()
    if not name or not email or not event:
        return jsonify(error="Name, email, and event are required."), 400
    if len(name) > 120 or len(email) > 254 or len(event) > 160:
        return jsonify(error="One or more registration fields are too long."), 400

    regno = os.environ.get("REGNO", "8074")
    try:
        with get_connection() as connection:
            ensure_registration_table(connection)
            row = connection.execute(
                """
                INSERT INTO registrations (name, email, event, regno)
                VALUES (%s, %s, %s, %s)
                RETURNING id, name, email, event, regno, created_at
                """,
                (name, email, event, regno),
            ).fetchone()
    except psycopg.Error:
        return jsonify(error="Registration service is unavailable."), 503

    return jsonify(
        registration={
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "event": row[3],
            "regno": row[4],
            "created_at": row[5].isoformat(),
        }
    ), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)