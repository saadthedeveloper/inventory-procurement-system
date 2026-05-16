import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def migrate():
    # Connect without database first (to create it if needed)
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    # Create database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")

    # Create migration tracking table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS migrations_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255) NOT NULL UNIQUE,
            ran_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Get already applied migrations
    cursor.execute("SELECT filename FROM migrations_log")
    applied = {row["filename"] for row in cursor.fetchall()}

    # Run new migrations in order
    migrations_dir = os.path.join(os.path.dirname(__file__), "migrations")
    files = sorted(os.listdir(migrations_dir))

    for filename in files:
        if filename.endswith(".sql") and filename not in applied:
            filepath = os.path.join(migrations_dir, filename)
            with open(filepath, "r") as f:
                sql = f.read()
            # Split by semicolon to execute multiple statements (if any)
            for statement in sql.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            cursor.execute("INSERT INTO migrations_log (filename) VALUES (%s)", (filename,))
            conn.commit()
            print(f"Ran: {filename}")
        else:
            print(f"Skipped (already applied): {filename}")

    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
