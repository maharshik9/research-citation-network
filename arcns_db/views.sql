USE arcns;

-- ─────────────────────────────────────────────────
-- V1: Top cited papers with author list
-- ─────────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_top_cited_papers AS
SELECT p.paper_id, p.title, p.year, p.doi,
       v.name AS venue,
       p.citation_count_cache AS citations,
       GROUP_CONCAT(r.name ORDER BY a.author_order SEPARATOR ', ') AS authors
FROM paper p
LEFT JOIN venue     v  ON v.venue_id     = p.venue_id
LEFT JOIN authorship a  ON a.paper_id     = p.paper_id
LEFT JOIN researcher r  ON r.researcher_id = a.researcher_id
GROUP BY p.paper_id;

-- ─────────────────────────────────────────────────
-- V2: Author leaderboard
-- ─────────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_author_leaderboard AS
SELECT r.researcher_id, r.name, r.email, r.h_index_cache,
       COUNT(DISTINCT a.paper_id) AS total_publications,
       SUM(p.citation_count_cache) AS total_citations
FROM researcher r
JOIN authorship a ON a.researcher_id = r.researcher_id
JOIN paper p      ON p.paper_id = a.paper_id
GROUP BY r.researcher_id;

-- ─────────────────────────────────────────────────
-- V3: Venue statistics
-- ─────────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_venue_stats AS
SELECT v.venue_id, v.name, v.type,
       COUNT(p.paper_id)               AS total_papers,
       ROUND(AVG(p.citation_count_cache),2) AS avg_citations,
       MAX(p.citation_count_cache)     AS max_citations
FROM venue v
LEFT JOIN paper p ON p.venue_id = v.venue_id
GROUP BY v.venue_id;

-- ─────────────────────────────────────────────────
-- V4: Collaboration pairs
-- ─────────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_collaborations AS
SELECT r1.researcher_id AS author_a_id, r1.name AS author_a,
       r2.researcher_id AS author_b_id, r2.name AS author_b,
       COUNT(DISTINCT a1.paper_id) AS collab_count
FROM authorship a1
JOIN authorship a2  ON a1.paper_id = a2.paper_id AND a1.researcher_id < a2.researcher_id
JOIN researcher r1  ON r1.researcher_id = a1.researcher_id
JOIN researcher r2  ON r2.researcher_id = a2.researcher_id
GROUP BY a1.researcher_id, a2.researcher_id;
