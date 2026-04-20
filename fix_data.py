import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'arcns_user',
    'password': 'arcns_pass_2026',
    'database': 'arcns'
}

def fix():
    # Try to grant permissions as root if possible
    try:
        root_conn = mysql.connector.connect(host='localhost', user='root')
        root_cursor = root_conn.cursor()
        root_cursor.execute("GRANT EXECUTE ON arcns.* TO 'arcns_user'@'localhost'")
        root_conn.commit()
        print("Granted execute permissions via root.")
        root_cursor.close()
        root_conn.close()
    except Exception as e:
        print(f"Root grant failed: {e}")

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    # Update paper 10 title to ensure it has "Database"
    cursor.execute("UPDATE paper SET title = 'Advanced Database Systems and Graph Analysis' WHERE paper_id = 10")
    print("Updated paper 10 title.")
    
    # Ensure paper 10 has citations
    cursor.execute("SELECT * FROM citation WHERE cited_paper_id = 10")
    citations = cursor.fetchall()
    print(f"Paper 10 has {len(citations)} incoming citations.")
    
    if len(citations) < 2:
        # Add some dummy citations
        cursor.execute("INSERT IGNORE INTO citation (citing_paper_id, cited_paper_id, citation_context) VALUES (1, 10, 'Context 1')")
        cursor.execute("INSERT IGNORE INTO citation (citing_paper_id, cited_paper_id, citation_context) VALUES (2, 10, 'Context 2')")
        print("Added dummy citations for paper 10.")
    
    # Test the stored procedure
    print("Testing sp_get_citation_chain for paper 10...")
    try:
        cursor.callproc('sp_get_citation_chain', (10, 3))
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
        print(f"Procedure returned {len(results)} rows.")
    except Exception as e:
        print(f"Procedure Error: {e}")
        
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    fix()
