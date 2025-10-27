# Database connection configuration
dbuser = "root"
dbpass = "Lincoln5673793"   # <-- Enter your MySQL Server password here 
                                # (NOT PRIVATE - don't re-use an important password you use elsewhere)
dbhost = "127.0.0.1"
dbport = 3306
dbname = "svs"


import mysql.connector

def get_connection():
    """Return a new MySQL connection using mysql.connector (Assignment 2 requirement)."""
    return mysql.connector.connect(
        host=dbhost,
        user=dbuser,
        password=dbpass,
        database=dbname,
        port=dbport
    )