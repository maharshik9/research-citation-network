import http.server
import socketserver
import json
import mysql.connector
from urllib.parse import urlparse, parse_qs

# DB Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'arcns_user',
    'password': 'arcns_pass_2026',
    'database': 'arcns'
}

PORT = 8000

class ARCNSHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/api/query':
            self.handle_query(parsed_path.query)
        elif parsed_path.path == '/api/stats':
            self.handle_stats()
        elif parsed_path.path == '/api/citation-chain':
            self.handle_citation_chain(parsed_path.query)
        else:
            super().do_GET()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/api/add-paper':
            self.handle_add_paper()

    def handle_query(self, query_string):
        params = parse_qs(query_string)
        query_key = params.get('type', [None])[0]
        search_term = params.get('q', [None])[0]

        # SQL Query Registry
        QUERIES = {
            'top_papers': "SELECT * FROM vw_top_cited_papers ORDER BY citations DESC LIMIT 10;",
            'author_leaderboard': "SELECT * FROM vw_author_leaderboard ORDER BY total_citations DESC LIMIT 10;",
            'keyword_trends': """
                SELECT kw.term AS keyword, p.year, COUNT(DISTINCT p.paper_id) AS paper_count
                FROM keyword kw
                JOIN paper_keyword pk ON pk.keyword_id = kw.keyword_id
                JOIN paper p ON p.paper_id = pk.paper_id
                GROUP BY kw.keyword_id, p.year
                ORDER BY paper_count DESC;
            """,
            'venue_rankings': "SELECT * FROM vw_venue_stats ORDER BY avg_citations DESC;",
            'collaborations': "SELECT * FROM vw_collaborations ORDER BY collab_count DESC LIMIT 20;",
            'institutional_output': """
                SELECT i.name AS institution, COUNT(DISTINCT p.paper_id) AS total_papers, SUM(p.citation_count_cache) AS total_citations
                FROM institution i
                JOIN researcher_affiliation ra ON ra.institution_id = i.institution_id
                JOIN authorship a ON a.researcher_id = ra.researcher_id
                JOIN paper p ON p.paper_id = a.paper_id
                WHERE p.year BETWEEN ra.start_year AND IFNULL(ra.end_year, YEAR(CURDATE()))
                GROUP BY i.institution_id
                ORDER BY total_citations DESC LIMIT 10;
            """,
            'keyword_cooccurrence': """
                SELECT k1.term AS kw1, k2.term AS kw2, COUNT(*) AS co_count
                FROM paper_keyword pk1
                JOIN paper_keyword pk2 ON pk1.paper_id = pk2.paper_id AND pk1.keyword_id < pk2.keyword_id
                JOIN keyword k1 ON k1.keyword_id = pk1.keyword_id
                JOIN keyword k2 ON k2.keyword_id = pk2.keyword_id
                GROUP BY pk1.keyword_id, pk2.keyword_id
                ORDER BY co_count DESC LIMIT 20;
            """,
            'search': f"SELECT paper_id, title, year, citation_count_cache AS citations FROM paper WHERE title LIKE %s OR abstract LIKE %s LIMIT 20;"
        }

        if not query_key or query_key not in QUERIES:
            self.send_api_error(400, "Invalid or missing query type")
            return

        sql = QUERIES[query_key]
        args = (f"%{search_term}%", f"%{search_term}%") if query_key == 'search' else None
        
        try:
            results = self.execute_sql(sql, args)
            self.send_api_json(results)
        except Exception as e:
            print(f"Query Error: {e}")
            self.send_api_error(500, str(e))

    def handle_stats(self):
        """Fetch high-level dashboard counts."""
        try:
            # Simplified for demo:
            stats = {
                'papers': self.execute_sql("SELECT COUNT(*) as count FROM paper")[0]['count'],
                'researchers': self.execute_sql("SELECT COUNT(*) as count FROM researcher")[0]['count'],
                'citations': self.execute_sql("SELECT COUNT(*) as total FROM citation")[0]['total'],
                'venues': self.execute_sql("SELECT COUNT(*) as count FROM venue")[0]['count']
            }
            self.send_api_json(stats)
        except Exception as e:
            print(f"Stats Error: {e}")
            self.send_api_error(500, str(e))

    def handle_citation_chain(self, query_string):
        params = parse_qs(query_string)
        paper_id = params.get('id', [None])[0]
        if not paper_id:
            self.send_api_error(400, "Paper ID required")
            return
        
        try:
            # Run the recursive CTE directly to avoid permission issues with stored procedures
            sql = """
                WITH RECURSIVE citation_path AS (
                    SELECT citing_paper_id AS source,
                           cited_paper_id  AS target,
                           1 AS depth
                    FROM citation
                    WHERE cited_paper_id = %s

                    UNION ALL

                    SELECT c.citing_paper_id, c.cited_paper_id, cp.depth + 1
                    FROM citation c
                    JOIN citation_path cp ON c.cited_paper_id = cp.source
                    WHERE cp.depth < 3
                )
                SELECT DISTINCT source, target, depth FROM citation_path;
            """
            results = self.execute_sql(sql, (int(paper_id),))
            self.send_api_json(results)
        except Exception as e:
            print(f"Chain Error: {e}")
            self.send_api_error(500, str(e))

    def handle_add_paper(self):
        """Demonstrate Transaction / Insert."""
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Start Transaction implicitly by connection settings, or explicitly:
            conn.start_transaction()
            
            sql = "INSERT INTO paper (title, abstract, year, venue_id) VALUES (%s, %s, %s, %s)"
            vals = (post_data['title'], post_data['abstract'], post_data['year'], post_data.get('venue_id'))
            cursor.execute(sql, vals)
            new_id = cursor.lastrowid
            
            conn.commit()
            cursor.close()
            conn.close()
            
            self.send_api_json({"status": "success", "id": new_id})
        except Exception as e:
            print(f"Insert Error: {e}")
            self.send_api_error(500, str(e))

    def execute_sql(self, sql, args=None):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def send_api_json(self, data):
        def convert(o):
            return str(o) if not isinstance(o, (str, int, float, bool, type(None))) else o

        json_response = json.dumps(data, default=convert)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json_response.encode())

    def send_api_error(self, code, message):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode())

if __name__ == "__main__":
    print(f"Starting ARCNS Server on http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), ARCNSHandler) as httpd:
        httpd.serve_forever()

