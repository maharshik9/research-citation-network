import mysql.connector
import os
import re

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'arcns_user',
    'password': 'arcns_pass_2026',
    'database': 'arcns'
}

def execute_script(cursor, filepath):
    print(f"Executing: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Handle custom delimiters ($$)
    # We look for DELIMITER $$ and capture everything until the next DELIMITER ;
    # This is common in triggers/procedures
    
    # Simple regex to split by ';' EXCEPT when it's part of a block
    # Actually, a better way for these files:
    # We can use the 'mysql-connector' cursor.execute with multiple=True
    # But it doesn't like the DELIMITER keyword
    
    # Clean up the file content: remove DELIMITER lines
    cleaned_content = re.sub(r'(?i)DELIMITER\s+\S+', '', content)
    # Replace the custom delimiter ($$) with the standard (;)
    # But ONLY if it's not inside a string. For our files, $$ is safe.
    cleaned_content = cleaned_content.replace('$$', ';')
    
    # Split by ;
    statements = cleaned_content.split(';')
    
    for statement in statements:
        stmt = statement.strip()
        if not stmt:
            continue
        try:
            # Skip 'USE' and 'DELIMITER'
            if stmt.upper().startswith('USE ') or stmt.upper().startswith('DELIMITER'):
                continue
            cursor.execute(stmt)
        except mysql.connector.Error as err:
            print(f"Error in {filepath}: {err}")
            # print(f"Statement: {stmt[:100]}...")

def initialize():
    scripts = [
        'arcns_db/schema.sql',
        'arcns_db/triggers.sql',
        'arcns_db/views.sql',
        'arcns_db/procedures.sql',
        'arcns_db/seed_data.sql'
    ]
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        for script in scripts:
            if os.path.exists(script):
                execute_script(cursor, script)
                conn.commit()
            else:
                print(f"Script not found: {script}")
        
        cursor.close()
        conn.close()
        print("\n✅ Database fully initialized with Schema, Triggers, Views, and Seed Data!")
    except Exception as e:
        print(f"❌ Critical Failure: {e}")

if __name__ == "__main__":
    initialize()
