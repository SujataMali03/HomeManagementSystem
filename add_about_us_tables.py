import sqlite3

DATABASE = "home_management.db"

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

# Our Story
cursor.execute("""
CREATE TABLE IF NOT EXISTS our_story (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Core Values
cursor.execute("""
CREATE TABLE IF NOT EXISTS core_values (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Programs
cursor.execute("""
CREATE TABLE IF NOT EXISTS programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Team Members
cursor.execute("""
CREATE TABLE IF NOT EXISTS team_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    image_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Default Our Story
if cursor.execute("SELECT COUNT(*) FROM our_story").fetchone()[0] == 0:
    cursor.execute("""
        INSERT INTO our_story (content)
        VALUES (?)
    """, (
        "We are committed to creating a better and brighter future by supporting communities through education, empowerment and sustainable development.",
    ))

# Default Core Values
if cursor.execute("SELECT COUNT(*) FROM core_values").fetchone()[0] == 0:
    cursor.executemany("""
        INSERT INTO core_values (value)
        VALUES (?)
    """, [
        ("Integrity",),
        ("Empathy",),
        ("Inclusivity",),
        ("Transparency",)
    ])

# Default Programs
if cursor.execute("SELECT COUNT(*) FROM programs").fetchone()[0] == 0:
    cursor.executemany("""
        INSERT INTO programs (name, description)
        VALUES (?, ?)
    """, [
        (
            "Child Education",
            "Providing educational resources and learning opportunities for children."
        ),
        (
            "Women Empowerment",
            "Supporting women through skill development and vocational training."
        ),
        (
            "Community Healthcare",
            "Supporting healthcare awareness and health programs in communities."
        )
    ])

# Default Team Members
if cursor.execute("SELECT COUNT(*) FROM team_members").fetchone()[0] == 0:
    cursor.executemany("""
        INSERT INTO team_members (name, role, image_url)
        VALUES (?, ?, ?)
    """, [
        ("NGO Founder", "Founder", ""),
        ("Program Coordinator", "Program Coordinator", "")
    ])

connection.commit()
connection.close()

print("About Us tables and default data created successfully!")