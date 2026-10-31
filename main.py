
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import sqlite3
import json

app = FastAPI(
    title="StudySpot API",
    description="An API for finding and managing study spaces.",
    version="1.0.0"
)

DATABASE = "studyspots.db"


# DATABASE SETUP

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def setup_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS studyspots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                noise_level INTEGER NOT NULL,
                busy_level INTEGER NOT NULL,
                has_wifi BOOLEAN NOT NULL,
                tags TEXT NOT NULL
            )
        """)


setup_database()


# DATA VALIDATION

class StudySpot(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    location: str = Field(min_length=2, max_length=100)
    noise_level: int = Field(ge=1, le=5)
    busy_level: int = Field(ge=1, le=5)
    has_wifi: bool
    tags: list[str] = []


# HELPER FUNCTION

def format_spot(spot):
    result = dict(spot)
    result["has_wifi"] = bool(result["has_wifi"])
    result["tags"] = json.loads(result["tags"])
    return result


# 1. HOME ENDPOINT

@app.get("/")
def home():
    return {
        "message": "Welcome to StudySpot API!",
        "documentation": "/docs"
    }


# 2. GET ALL STUDY SPACES

@app.get("/spots")
def get_spots(
    max_noise: int | None = None,
    max_busy: int | None = None
):
    query = "SELECT * FROM studyspots WHERE 1=1"
    parameters = []

    if max_noise is not None:
        query += " AND noise_level <= ?"
        parameters.append(max_noise)

    if max_busy is not None:
        query += " AND busy_level <= ?"
        parameters.append(max_busy)

    with get_connection() as connection:
        spots = connection.execute(
            query, parameters
        ).fetchall()

    return [format_spot(spot) for spot in spots]


# 3. GET ONE STUDY SPACE

@app.get("/spots/{spot_id}")
def get_spot(spot_id: int):
    with get_connection() as connection:
        spot = connection.execute(
            "SELECT * FROM studyspots WHERE id = ?",
            (spot_id,)
        ).fetchone()

    if spot is None:
        raise HTTPException(
            status_code=404,
            detail="Study space not found"
        )

    return format_spot(spot)


# 4. CREATE A STUDY SPACE

@app.post("/spots", status_code=201)
def create_spot(spot: StudySpot):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO studyspots
            (name, location, noise_level,
             busy_level, has_wifi, tags)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                spot.name,
                spot.location,
                spot.noise_level,
                spot.busy_level,
                spot.has_wifi,
                json.dumps(spot.tags)
            )
        )

        spot_id = cursor.lastrowid

    return get_spot(spot_id)


# 5. UPDATE A STUDY SPACE

@app.put("/spots/{spot_id}")
def update_spot(spot_id: int, spot: StudySpot):
    with get_connection() as connection:
        existing = connection.execute(
            "SELECT id FROM studyspots WHERE id = ?",
            (spot_id,)
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Study space not found"
            )

        connection.execute(
            """
            UPDATE studyspots
            SET name = ?, location = ?,
                noise_level = ?, busy_level = ?,
                has_wifi = ?, tags = ?
            WHERE id = ?
            """,
            (
                spot.name,
                spot.location,
                spot.noise_level,
                spot.busy_level,
                spot.has_wifi,
                json.dumps(spot.tags),
                spot_id
            )
        )

    return get_spot(spot_id)


# 6. DELETE A STUDY SPACE

@app.delete("/spots/{spot_id}")
def delete_spot(spot_id: int):
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM studyspots WHERE id = ?",
            (spot_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Study space not found"
            )

    return {"message": "Study space deleted successfully"}