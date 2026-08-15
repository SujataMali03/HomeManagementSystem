from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from database import get_db_connection, init_database


app = Flask(__name__)

# =========================================================
# SECRET KEY
# =========================================================

app.secret_key = "home-management-secret-key"


# =========================================================
# INITIALIZE DATABASE
# =========================================================

init_database()


# =========================================================
# PUBLIC HOME PAGE
# =========================================================

@app.route("/")
def home():

    connection = get_db_connection()

    # -----------------------------------------------------
    # Get active banners
    # -----------------------------------------------------

    banners = connection.execute(
        """
        SELECT *
        FROM banners
        WHERE status = 1
        ORDER BY display_order
        """
    ).fetchall()


    # -----------------------------------------------------
    # Get Vision & Mission
    # -----------------------------------------------------

    vision_mission = connection.execute(
        """
        SELECT *
        FROM vision_mission
        LIMIT 1
        """
    ).fetchone()


    # -----------------------------------------------------
    # Get active statistics
    # -----------------------------------------------------

    statistics = connection.execute(
        """
        SELECT *
        FROM statistics
        WHERE status = 1
        ORDER BY display_order
        """
    ).fetchall()


    # -----------------------------------------------------
    # Get active initiatives
    # -----------------------------------------------------

    initiatives = connection.execute(
        """
        SELECT *
        FROM initiatives
        WHERE status = 1
        ORDER BY display_order
        """
    ).fetchall()


    connection.close()


    return render_template(
        "home.html",
        banners=banners,
        vision_mission=vision_mission,
        statistics=statistics,
        initiatives=initiatives
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    error = None


    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")


        connection = get_db_connection()


        user = connection.execute(
            """
            SELECT *
            FROM users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()


        connection.close()


        if user and check_password_hash(
            user["password"],
            password
        ):

            session["admin_logged_in"] = True
            session["admin_username"] = user["username"]


            return redirect(
                url_for("admin_dashboard")
            )


        else:

            error = "Invalid username or password."


    return render_template(
        "login.html",
        error=error
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin/dashboard")
def admin_dashboard():

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )


    return render_template(
        "dashboard.html",
        username=session.get("admin_username")
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin/logout")
def admin_logout():

    session.clear()

    return redirect(
        url_for("admin_login")
    )


# =========================================================
# BANNER MANAGEMENT
# =========================================================

@app.route("/admin/banners")
def manage_banners():

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )


    connection = get_db_connection()


    banners = connection.execute(
        """
        SELECT *
        FROM banners
        ORDER BY display_order
        """
    ).fetchall()


    connection.close()


    return render_template(
        "banners.html",
        banners=banners
    )


# ---------------------------------------------------------
# ADD BANNER
# ---------------------------------------------------------

@app.route(
    "/admin/banners/add",
    methods=["GET", "POST"]
)
def add_banner():

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )


    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        image_url = request.form.get("image_url")
        display_order = request.form.get("display_order")
        status = request.form.get("status")


        connection = get_db_connection()


        connection.execute(
            """
            INSERT INTO banners
            (
                title,
                description,
                image_url,
                display_order,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                title,
                description,
                image_url,
                display_order,
                status
            )
        )


        connection.commit()
        connection.close()


        return redirect(
            url_for("manage_banners")
        )


    return render_template(
        "add_banner.html"
    )


# ---------------------------------------------------------
# EDIT BANNER
# ---------------------------------------------------------

@app.route(
    "/admin/banners/edit/<int:banner_id>",
    methods=["GET", "POST"]
)
def edit_banner(banner_id):

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )


    connection = get_db_connection()


    banner = connection.execute(
        """
        SELECT *
        FROM banners
        WHERE id = ?
        """,
        (banner_id,)
    ).fetchone()


    if banner is None:

        connection.close()

        return "Banner not found", 404


    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        image_url = request.form.get("image_url")
        display_order = request.form.get("display_order")
        status = request.form.get("status")


        connection.execute(
            """
            UPDATE banners

            SET
                title = ?,
                description = ?,
                image_url = ?,
                display_order = ?,
                status = ?

            WHERE id = ?
            """,
            (
                title,
                description,
                image_url,
                display_order,
                status,
                banner_id
            )
        )


        connection.commit()
        connection.close()


        return redirect(
            url_for("manage_banners")
        )


    connection.close()


    return render_template(
        "edit_banner.html",
        banner=banner
    )


# ---------------------------------------------------------
# DELETE BANNER
# ---------------------------------------------------------

@app.route(
    "/admin/banners/delete/<int:banner_id>"
)
def delete_banner(banner_id):

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )


    connection = get_db_connection()


    connection.execute(
        """
        DELETE FROM banners
        WHERE id = ?
        """,
        (banner_id,)
    )


    connection.commit()
    connection.close()


    return redirect(
        url_for("manage_banners")
    )


# =========================================================
# VISION & MISSION MANAGEMENT
# =========================================================

@app.route(
    "/admin/vision-mission",
    methods=["GET", "POST"]
)
def manage_vision_mission():

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )


    connection = get_db_connection()


    data = connection.execute(
        """
        SELECT *
        FROM vision_mission
        LIMIT 1
        """
    ).fetchone()


    # Create default record if none exists

    if data is None:

        connection.execute(
            """
            INSERT INTO vision_mission
            (
                vision_title,
                vision_description,
                mission_title,
                mission_description
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                "Our Vision",
                "Our vision is to create a better future.",
                "Our Mission",
                "Our mission is to work together for positive development."
            )
        )


        connection.commit()


        data = connection.execute(
            """
            SELECT *
            FROM vision_mission
            LIMIT 1
            """
        ).fetchone()


    # -----------------------------------------------------
    # UPDATE VISION & MISSION
    # -----------------------------------------------------

    if request.method == "POST":

        vision_title = request.form.get(
            "vision_title"
        )

        vision_description = request.form.get(
            "vision_description"
        )

        mission_title = request.form.get(
            "mission_title"
        )

        mission_description = request.form.get(
            "mission_description"
        )


        if not vision_title:

            vision_title = "Our Vision"


        if not vision_description:

            vision_description = ""


        if not mission_title:

            mission_title = "Our Mission"


        if not mission_description:

            mission_description = ""


        connection.execute(
            """
            UPDATE vision_mission

            SET
                vision_title = ?,
                vision_description = ?,
                mission_title = ?,
                mission_description = ?

            WHERE id = ?
            """,
            (
                vision_title,
                vision_description,
                mission_title,
                mission_description,
                data["id"]
            )
        )


        connection.commit()


        data = connection.execute(
            """
            SELECT *
            FROM vision_mission
            WHERE id = ?
            """,
            (data["id"],)
        ).fetchone()


        connection.close()


        return render_template(
            "vision_mission.html",
            data=data,
            success="Vision and Mission updated successfully!"
        )


    connection.close()


    return render_template(
        "vision_mission.html",
        data=data
    )


# =========================================================
# STATISTICS MANAGEMENT
# =========================================================

@app.route("/admin/statistics")
def manage_statistics():

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )


    connection = get_db_connection()


    statistics = connection.execute(
        """
        SELECT *
        FROM statistics
        ORDER BY display_order
        """
    ).fetchall()


    connection.close()


    return render_template(
        "statistics.html",
        statistics=statistics
    )


# ---------------------------------------------------------
# ADD STATISTIC
# ---------------------------------------------------------

@app.route(
    "/admin/statistics/add",
    methods=["GET", "POST"]
)
def add_statistic():

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )


    if request.method == "POST":

        label = request.form.get("label")
        value = request.form.get("value")
        display_order = request.form.get("display_order")
        status = request.form.get("status")


        connection = get_db_connection()


        connection.execute(
            """
            INSERT INTO statistics
            (
                label,
                value,
                display_order,
                status
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                label,
                value,
                display_order,
                status
            )
        )


        connection.commit()
        connection.close()


        return redirect(
            url_for("manage_statistics")
        )


    return render_template(
        "add_statistic.html"
    )


# ---------------------------------------------------------
# EDIT STATISTIC
# ---------------------------------------------------------

@app.route(
    "/admin/statistics/edit/<int:statistic_id>",
    methods=["GET", "POST"]
)
def edit_statistic(statistic_id):

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )


    connection = get_db_connection()


    statistic = connection.execute(
        """
        SELECT *
        FROM statistics
        WHERE id = ?
        """,
        (statistic_id,)
    ).fetchone()


    if statistic is None:

        connection.close()

        return "Statistic not found", 404


    if request.method == "POST":

        label = request.form.get("label")
        value = request.form.get("value")
        display_order = request.form.get("display_order")
        status = request.form.get("status")


        connection.execute(
            """
            UPDATE statistics

            SET
                label = ?,
                value = ?,
                display_order = ?,
                status = ?

            WHERE id = ?
            """,
            (
                label,
                value,
                display_order,
                status,
                statistic_id
            )
        )


        connection.commit()
        connection.close()


        return redirect(
            url_for("manage_statistics")
        )


    connection.close()


    return render_template(
        "edit_statistic.html",
        statistic=statistic
    )


# ---------------------------------------------------------
# DELETE STATISTIC
# ---------------------------------------------------------

@app.route(
    "/admin/statistics/delete/<int:statistic_id>"
)
def delete_statistic(statistic_id):

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )


    connection = get_db_connection()


    connection.execute(
        """
        DELETE FROM statistics
        WHERE id = ?
        """,
        (statistic_id,)
    )


    connection.commit()
    connection.close()


    return redirect(
        url_for("manage_statistics")
    )


# =========================================================
# INITIATIVES MANAGEMENT
# =========================================================

@app.route("/admin/initiatives")
def manage_initiatives():

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )


    connection = get_db_connection()


    initiatives = connection.execute(
        """
        SELECT *
        FROM initiatives
        ORDER BY display_order
        """
    ).fetchall()


    connection.close()


    return render_template(
        "initiatives.html",
        initiatives=initiatives
    )


# ---------------------------------------------------------
# ADD INITIATIVE
# ---------------------------------------------------------

@app.route(
    "/admin/initiatives/add",
    methods=["GET", "POST"]
)
def add_initiative():

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )


    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        display_order = request.form.get("display_order")
        status = request.form.get("status")


        connection = get_db_connection()


        connection.execute(
            """
            INSERT INTO initiatives
            (
                title,
                description,
                display_order,
                status
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                title,
                description,
                display_order,
                status
            )
        )


        connection.commit()
        connection.close()


        return redirect(
            url_for("manage_initiatives")
        )


    return render_template(
        "add_initiative.html"
    )


# ---------------------------------------------------------
# EDIT INITIATIVE
# ---------------------------------------------------------

@app.route(
    "/admin/initiatives/edit/<int:initiative_id>",
    methods=["GET", "POST"]
)
def edit_initiative(initiative_id):

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )


    connection = get_db_connection()


    initiative = connection.execute(
        """
        SELECT *
        FROM initiatives
        WHERE id = ?
        """,
        (initiative_id,)
    ).fetchone()


    if initiative is None:

        connection.close()

        return "Initiative not found", 404


    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        display_order = request.form.get("display_order")
        status = request.form.get("status")


        connection.execute(
            """
            UPDATE initiatives

            SET
                title = ?,
                description = ?,
                display_order = ?,
                status = ?

            WHERE id = ?
            """,
            (
                title,
                description,
                display_order,
                status,
                initiative_id
            )
        )


        connection.commit()
        connection.close()


        return redirect(
            url_for("manage_initiatives")
        )


    connection.close()


    return render_template(
        "edit_initiative.html",
        initiative=initiative
    )


# ---------------------------------------------------------
# DELETE INITIATIVE
# ---------------------------------------------------------

@app.route(
    "/admin/initiatives/delete/<int:initiative_id>"
)
def delete_initiative(initiative_id):

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )


    connection = get_db_connection()


    connection.execute(
        """
        DELETE FROM initiatives
        WHERE id = ?
        """,
        (initiative_id,)
    )


    connection.commit()
    connection.close()


    return redirect(
        url_for("manage_initiatives")
    )

# =========================================================
# ABOUT US MANAGEMENT
# =========================================================
# =========================================================
# PUBLIC ABOUT US
# =========================================================

@app.route("/about-us")
def about_us():

    connection = get_db_connection()

    story = connection.execute(
        "SELECT * FROM our_story LIMIT 1"
    ).fetchone()

    values = connection.execute(
        "SELECT * FROM core_values ORDER BY id"
    ).fetchall()

    programs = connection.execute(
        "SELECT * FROM programs ORDER BY id"
    ).fetchall()

    team_members = connection.execute(
        "SELECT * FROM team_members ORDER BY id"
    ).fetchall()

    connection.close()

    return render_template(
        "about_us.html",
        story=story,
        values=values,
        programs=programs,
        team_members=team_members
    )


# =========================================================
# ADMIN ABOUT US
# =========================================================
@app.route("/admin/about-us", methods=["GET", "POST"])
def manage_about_us():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = get_db_connection()

    if request.method == "POST":

        section = request.form.get("section")

        # -------------------------
        # OUR STORY
        # -------------------------
        if section == "story":

            content = request.form.get("content")

            connection.execute("""
                UPDATE our_story
                SET content = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = 1
            """, (content,))

        # -------------------------
        # CORE VALUE
        # -------------------------
        elif section == "value":

            value = request.form.get("value")

            if value:
                connection.execute("""
                    INSERT INTO core_values (value)
                    VALUES (?)
                """, (value,))

        # -------------------------
        # PROGRAM
        # -------------------------
        elif section == "program":

            name = request.form.get("name")
            description = request.form.get("description")

            if name:
                connection.execute("""
                    INSERT INTO programs (name, description)
                    VALUES (?, ?)
                """, (name, description))

        # -------------------------
        # TEAM MEMBER
        # -------------------------
        elif section == "team":

            name = request.form.get("name")
            role = request.form.get("role")
            image_url = request.form.get("image_url")

            if name and role:

                connection.execute("""
                    INSERT INTO team_members
                    (name, role, image_url)
                    VALUES (?, ?, ?)
                """, (name, role, image_url))

        connection.commit()

    # Get Our Story
    story = connection.execute("""
        SELECT *
        FROM our_story
        WHERE id = 1
    """).fetchone()

    # Get Core Values
    values = connection.execute("""
        SELECT *
        FROM core_values
        ORDER BY id
    """).fetchall()

    # Get Programs
    programs = connection.execute("""
        SELECT *
        FROM programs
        ORDER BY id
    """).fetchall()

    # Get Team Members
    team_members = connection.execute("""
        SELECT *
        FROM team_members
        ORDER BY id
    """).fetchall()

    connection.close()

    return render_template(
        "about_us_admin.html",
        story=story,
        values=values,
        programs=programs,
        team_members=team_members
    )


# =========================================================
# DELETE CORE VALUE
# =========================================================

@app.route("/admin/about-us/value/delete/<int:value_id>")
def delete_core_value(value_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM core_values WHERE id = ?",
        (value_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("manage_about_us"))


# =========================================================
# DELETE PROGRAM
# =========================================================

@app.route("/admin/about-us/program/delete/<int:program_id>")
def delete_program(program_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM programs WHERE id = ?",
        (program_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("manage_about_us"))


# =========================================================
# DELETE TEAM MEMBER
# =========================================================

@app.route("/admin/about-us/team/delete/<int:team_id>")
def delete_team_member(team_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM team_members WHERE id = ?",
        (team_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("manage_about_us"))


# =========================================================
# MEDIA MANAGEMENT
# =========================================================

@app.route("/admin/media")
def manage_media():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = get_db_connection()

    press_releases = connection.execute(
        "SELECT * FROM press_releases ORDER BY release_date DESC"
    ).fetchall()

    media_coverage = connection.execute(
        "SELECT * FROM media_coverage ORDER BY created_at DESC"
    ).fetchall()

    images = connection.execute(
        "SELECT * FROM image_gallery ORDER BY uploaded_at DESC"
    ).fetchall()

    videos = connection.execute(
        "SELECT * FROM videos ORDER BY uploaded_at DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "media_admin.html",
        press_releases=press_releases,
        media_coverage=media_coverage,
        images=images,
        videos=videos
    )


# =========================================================
# PUBLIC MEDIA
# =========================================================

@app.route("/media")
def media():

    connection = get_db_connection()

    press_releases = connection.execute(
        "SELECT * FROM press_releases ORDER BY release_date DESC"
    ).fetchall()

    media_coverage = connection.execute(
        "SELECT * FROM media_coverage ORDER BY created_at DESC"
    ).fetchall()

    images = connection.execute(
        "SELECT * FROM image_gallery ORDER BY uploaded_at DESC"
    ).fetchall()

    videos = connection.execute(
        "SELECT * FROM videos ORDER BY uploaded_at DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "media.html",
        press_releases=press_releases,
        media_coverage=media_coverage,
        images=images,
        videos=videos
    )

# =========================================================
# PRESS RELEASES
# =========================================================

@app.route("/admin/media/press-release/add", methods=["GET", "POST"])
def add_press_release():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        release_date = request.form.get("release_date")

        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO press_releases
            (title, description, release_date)
            VALUES (?, ?, ?)
            """,
            (title, description, release_date)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("manage_media"))

    return render_template("add_press_release.html")
# =========================================================
# EDIT PRESS RELEASE
# =========================================================

@app.route(
    "/admin/media/press-release/edit/<int:press_release_id>",
    methods=["GET", "POST"]
)
def edit_press_release(press_release_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = get_db_connection()

    press_release = connection.execute(
        "SELECT * FROM press_releases WHERE id = ?",
        (press_release_id,)
    ).fetchone()

    if press_release is None:
        connection.close()
        return "Press release not found", 404

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        release_date = request.form.get("release_date")

        connection.execute(
            """
            UPDATE press_releases
            SET title = ?,
                description = ?,
                release_date = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                title,
                description,
                release_date,
                press_release_id
            )
        )

        connection.commit()
        connection.close()

        return redirect(url_for("manage_media"))

    connection.close()

    return render_template(
        "edit_press_release.html",
        press_release=press_release
    )


# =========================================================
# DELETE PRESS RELEASE
# =========================================================

@app.route(
    "/admin/media/press-release/delete/<int:press_release_id>"
)
def delete_press_release(press_release_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM press_releases WHERE id = ?",
        (press_release_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("manage_media"))
# =========================================================
# MEDIA COVERAGE
# =========================================================

@app.route("/admin/media/coverage/add", methods=["GET", "POST"])
def add_media_coverage():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":

        title = request.form.get("title")
        url = request.form.get("url")

        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO media_coverage
            (title, url)
            VALUES (?, ?)
            """,
            (title, url)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("manage_media"))

    return render_template("add_media_coverage.html")

# =========================================================
# EDIT MEDIA COVERAGE
# =========================================================

@app.route(
    "/admin/media/coverage/edit/<int:coverage_id>",
    methods=["GET", "POST"]
)
def edit_media_coverage(coverage_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = get_db_connection()

    coverage = connection.execute(
        "SELECT * FROM media_coverage WHERE id = ?",
        (coverage_id,)
    ).fetchone()

    if coverage is None:
        connection.close()
        return "Media coverage not found", 404

    if request.method == "POST":

        title = request.form.get("title")
        url = request.form.get("url")

        connection.execute(
            """
            UPDATE media_coverage
            SET title = ?,
                url = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (title, url, coverage_id)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("manage_media"))

    connection.close()

    return render_template(
        "edit_media_coverage.html",
        coverage=coverage
    )

# =========================================================
# DELETE MEDIA COVERAGE
# =========================================================

@app.route("/admin/media/coverage/delete/<int:coverage_id>")
def delete_media_coverage(coverage_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM media_coverage WHERE id = ?",
        (coverage_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("manage_media"))
# =========================================================
# ADD MEDIA IMAGE
# =========================================================

@app.route("/admin/media/image/add", methods=["GET", "POST"])
def add_media_image():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":

        image_path = request.form.get("image_path")
        description = request.form.get("description")

        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO image_gallery
            (image_path, description)
            VALUES (?, ?)
            """,
            (image_path, description)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("manage_media"))

    return render_template("add_media_image.html")
# =========================================================
# DELETE MEDIA IMAGE
# =========================================================

@app.route("/admin/media/image/delete/<int:image_id>")
def delete_media_image(image_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM image_gallery WHERE id = ?",
        (image_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("manage_media"))
# =========================================================
# ADD MEDIA VIDEO
# =========================================================

@app.route("/admin/media/video/add", methods=["GET", "POST"])
def add_media_video():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":

        video_url = request.form.get("video_url")
        description = request.form.get("description")

        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO videos
            (video_url, description)
            VALUES (?, ?)
            """,
            (video_url, description)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("manage_media"))

    return render_template("add_media_video.html")

# =========================================================
# DELETE MEDIA VIDEO
# =========================================================

@app.route("/admin/media/video/delete/<int:video_id>")
def delete_media_video(video_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM videos WHERE id = ?",
        (video_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("manage_media"))
# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)
