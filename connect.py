# Database connection configuration
dbuser = "HanGu1171257"
dbpass = "Lincoln5673793"   # <-- Enter your MySQL Server password here
                                # (NOT PRIVATE - don't re-use an important password you use elsewhere)
dbhost = "HanGu1171257.mysql.pythonanywhere-services.com"
dbport = 3306
dbname = "HanGu1171257$svs"


import mysql.connector

def get_connection():
     return pymysql.connect(
        host=dbhost,
        user=dbuser,
        password=dbpass,
        database=dbname,
        port=dbport,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )