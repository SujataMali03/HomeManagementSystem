import sqlite3
from werkzeug.security import generate_password_hash


DATABASE = "home_management.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():

    connection = get_db_connection()

    cursor = connection.cursor()

    # Admin users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Banner table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS banners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            image_url TEXT,
            display_order INTEGER DEFAULT 1,
            status INTEGER DEFAULT 1
        )
    """)

    # Vision and Mission table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vision_mission (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vision_title TEXT NOT NULL,
            vision_description TEXT NOT NULL,
            mission_title TEXT NOT NULL,
            mission_description TEXT NOT NULL
        )
    """)

    # Statistics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            value TEXT NOT NULL,
            display_order INTEGER DEFAULT 1,
            status INTEGER DEFAULT 1
        )
    """)

    # Initiatives table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS initiatives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            image_url TEXT,
            display_order INTEGER DEFAULT 1,
            status INTEGER DEFAULT 1
        )
    """)

    # Create default admin account
    existing_admin = cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        ("admin",)
    ).fetchone()

    if existing_admin is None:

        password_hash = generate_password_hash("Admin@12345")

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", password_hash)
        )

    # Add default Vision and Mission
    existing_vision = cursor.execute(
        "SELECT id FROM vision_mission LIMIT 1"
    ).fetchone()

    if existing_vision is None:

        cursor.execute("""
            INSERT INTO vision_mission
            (
                vision_title,
                vision_description,
                mission_title,
                mission_description
            )
            VALUES (?, ?, ?, ?)
        """, (
            "Our Vision",
            "To create a better future by providing opportunities, education and support to communities.",
            "Our Mission",
            "To work together with communities and individuals to create meaningful and sustainable development."
        ))

    # Add default statistics
    existing_statistics = cursor.execute(
        "SELECT id FROM statistics LIMIT 1"
    ).fetchone()

    if existing_statistics is None:

        statistics = [
            ("Students Educated", "10,000+", 1),
            ("Projects Completed", "50+", 2),
            ("Volunteers", "500+", 3),
            ("Communities Served", "25+", 4)
        ]

        cursor.executemany("""
            INSERT INTO statistics
            (label, value, display_order)
            VALUES (?, ?, ?)
        """, statistics)

    # Add default initiatives
    existing_initiatives = cursor.execute(
        "SELECT id FROM initiatives LIMIT 1"
    ).fetchone()

    if existing_initiatives is None:

        initiatives = [
            (
                "Education",
                "Supporting education and learning opportunities for students.",
                "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=800&q=80",
                1
            ),
            (
                "Community Development",
                "Working with communities to improve quality of life.",
                "https://images.unsplash.com/photo-1532629345422-7515f3d16bb6?auto=format&fit=crop&w=800&q=80",
                2
            ),
            (
                "Environment",
                "Promoting environmental awareness and sustainable practices.",
                "https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9?auto=format&fit=crop&w=800&q=80",
                3
            )
        ]

        cursor.executemany("""
            INSERT INTO initiatives
            (title, description, image_url, display_order)
            VALUES (?, ?, ?, ?)
        """, initiatives)

    connection.commit()

    connection.close()


if __name__ == "__main__":
    init_database()
    print("Database created successfully!")