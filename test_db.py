import mysql.connector
import json

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'arcns_user',
    'password': 'arcns_pass_2026',
    'database': 'arcns'
}

def test_connection():
    try:
        print(f"Connecting to {DB_CONFIG['database']} on {DB_CONFIG['host']} as {DB_CONFIG['user']}...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Check if basic tables exist
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"Connection Successful! Tables found: {[t.get('Tables_in_arcns') for t in tables]}")
        
        # Try a sample query
        cursor.execute("SELECT COUNT(*) as count FROM paper")
        count = cursor.fetchone()
        print(f"Paper count: {count['count']}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    test_connection()
