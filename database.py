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

    # ============================================================
    # ADMIN USERS TABLE
    # ============================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # ============================================================
    # BANNER TABLE
    # ============================================================

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

    # ============================================================
    # VISION AND MISSION TABLE
    # ============================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vision_mission (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vision_title TEXT NOT NULL,
            vision_description TEXT NOT NULL,
            mission_title TEXT NOT NULL,
            mission_description TEXT NOT NULL
        )
    """)

    # ============================================================
    # STATISTICS TABLE
    # ============================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            value TEXT NOT NULL,
            display_order INTEGER DEFAULT 1,
            status INTEGER DEFAULT 1
        )
    """)

    # ============================================================
    # INITIATIVES TABLE
    # ============================================================

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

    # ============================================================
    # MEDIA MANAGEMENT TABLES
    # ============================================================

    # Press Releases
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS press_releases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            release_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Media Coverage
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS media_coverage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Image Gallery
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS image_gallery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT NOT NULL,
            description TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Videos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_url TEXT NOT NULL,
            description TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ============================================================
    # DEFAULT ADMIN ACCOUNT
    # ============================================================

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

    # ============================================================
    # DEFAULT VISION AND MISSION
    # ============================================================

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

    # ============================================================
    # DEFAULT STATISTICS
    # ============================================================

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

    # ============================================================
    # DEFAULT INITIATIVES
    # ============================================================

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

    # ============================================================
    # SAVE DATABASE CHANGES
    # ============================================================

    connection.commit()
    connection.close()


# ============================================================
# RUN DATABASE INITIALIZATION
# ============================================================

if __name__ == "__main__":
    init_database()
    print("Database created successfully!")