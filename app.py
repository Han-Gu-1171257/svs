from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from db import init_db, get_cursor

app = Flask(__name__)
app.secret_key = "svs_secret_key_2025"

# -------------------------------
# Database Configuration
# -------------------------------
init_db(
    app,
    user="HanGu1171257",
    password="Lincoln5673793",
    host="HanGu1171257.mysql.pythonanywhere-services.com",
    database="HanGu1171257$svs",
    port=3306
)

# -------------------------------
# Utility Functions
# -------------------------------
def money(value):
    try:
        return f"${float(value):,.2f}"
    except Exception:
        return "$0.00"

def fetch_all(sql, params=None):
    cur = get_cursor()
    cur.execute(sql, params or ())
    rows = cur.fetchall()
    cur.close()
    return rows

# -------------------------------
# Routes
# -------------------------------

@app.route("/")
def home():
    """Home page with image and current date"""
    return render_template("home.html", title="Home", curr_date=datetime.now())

@app.route("/services")
def services():
    """List all services"""
    rows = fetch_all("SELECT service_id, service_name, price FROM services ORDER BY service_name;")
    return render_template("service_list.html", title="Services", services=rows, money=money)

@app.route("/customers")
def customers():
    """Customer list with search"""
    q = request.args.get("q", "")
    if q:
        rows = fetch_all(
            "SELECT * FROM customers WHERE first_name LIKE %s OR family_name LIKE %s ORDER BY family_name, first_name;",
            (f"%{q}%", f"%{q}%")
        )
    else:
        rows = fetch_all("SELECT * FROM customers ORDER BY family_name, first_name;")
    return render_template("customer_list.html", title="Customers", customers=rows)

@app.route("/customers/<int:customer_id>")
def customer_summary(customer_id):
    """Customer detail and their appointments"""
    customer = fetch_all("SELECT * FROM customers WHERE customer_id = %s;", (customer_id,))
    if not customer:
        flash("Customer not found.", "warning")
        return redirect(url_for("customers"))
    customer = customer[0]

    appts = fetch_all("""
        SELECT a.appt_id, a.appt_datetime, a.notes, SUM(s.price) AS total_price
        FROM appointments a
        LEFT JOIN appointment_services aps ON a.appt_id = aps.appt_id
        LEFT JOIN services s ON aps.service_id = s.service_id
        WHERE a.customer_id = %s
        GROUP BY a.appt_id, a.appt_datetime, a.notes
        ORDER BY a.appt_datetime DESC;
    """, (customer_id,))

    return render_template("customer_summary.html", title="Customer Detail",
                           customer=customer, appointments=appts, money=money)

@app.route("/appointments")
def appointments():
    """Show all appointments with future highlight"""
    rows = fetch_all("""
        SELECT a.appt_id, a.appt_datetime, a.notes,
               CONCAT(c.first_name, ' ', c.family_name) AS customer_name,
               SUM(s.price) AS total_price
        FROM appointments a
        JOIN customers c ON a.customer_id = c.customer_id
        LEFT JOIN appointment_services aps ON a.appt_id = aps.appt_id
        LEFT JOIN services s ON aps.service_id = s.service_id
        GROUP BY a.appt_id, a.appt_datetime, a.notes, c.first_name, c.family_name
        ORDER BY a.appt_datetime DESC;
    """)
    return render_template("appointment_list.html", title="Appointments",
                           appts=rows, money=money, now=datetime.now())


@app.route("/appointments/add", methods=["GET", "POST"])
def add_appointment():
    """Add new appointment (no Sundays allowed)"""
    cur = get_cursor()
    cur.execute("SELECT customer_id, first_name, family_name FROM customers ORDER BY family_name;")
    customers = cur.fetchall()
    cur.execute("SELECT service_id, service_name, price FROM services ORDER BY service_name;")
    services = cur.fetchall()
    cur.close()

    if request.method == "POST":
        try:
            customer_id = int(request.form["customer_id"])
            date_str = request.form["date"]
            time_str = request.form["time"]
            selected_services = request.form.getlist("services")
            notes = request.form.get("notes", "").strip()   # ✅ 获取 notes 文本
            appt_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")


            if appt_datetime.weekday() == 6:
                flash("Appointments cannot be booked on Sunday.", "danger")
                return redirect(url_for("add_appointment"))


            cur = get_cursor()
            cur.execute(
                "INSERT INTO appointments (customer_id, appt_datetime, notes) VALUES (%s, %s, %s);",
                (customer_id, appt_datetime, notes)
            )
            cur.execute("SELECT LAST_INSERT_ID() AS new_id;")
            appt_id = cur.fetchone()["new_id"]


            for sid in selected_services:
                cur.execute(
                    "INSERT INTO appointment_services (appt_id, service_id) VALUES (%s, %s);",
                    (appt_id, sid)
                )

            cur.connection.commit()
            flash("✅ Appointment added successfully!", "success")
            return redirect(url_for("appointments"))

        except Exception as e:
            flash(f"Error adding appointment: {e}", "danger")

    return render_template("appointment_add.html", title="Add Appointment",
                           customers=customers, services=services, money=money)


# -------------------------------
# Template Context
# -------------------------------
@app.context_processor
def inject_now():
    """Make datetime.now() available in templates"""
    return {"now": datetime.now, "theme": "dark" if 18 <= datetime.now().hour or datetime.now().hour < 7 else "light"}

# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)


















