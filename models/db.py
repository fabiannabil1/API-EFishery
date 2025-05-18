import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host="localhost",
        dbname="lelangdb",
        user="postgres",
        password="010105",
    )
