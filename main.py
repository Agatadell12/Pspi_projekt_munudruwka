from GUI import gui
import psycopg2

db_params = psycopg2.connect(
    database='postgres',
    user='postgres',
    password='Psip_2023',
    host='localhost',
    port=5432
)

gui(db_params)
