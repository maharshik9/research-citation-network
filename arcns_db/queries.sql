USE arcns;

-- Q1: Top 10 Most Cited Papers
SELECT * FROM vw_top_cited_papers ORDER BY citations DESC LIMIT 10;

-- Q2: Author Leaderboard (by Citations)
SELECT * FROM vw_author_leaderboard ORDER BY total_citations DESC LIMIT 10;

-- Q3: Keyword Trends (Papers per Year)
SELECT kw.term AS keyword, p.year,
       COUNT(DISTINCT p.paper_id) AS paper_count
FROM keyword kw
JOIN paper_keyword pk ON pk.keyword_id = kw.keyword_id
JOIN paper p           ON p.paper_id   = pk.paper_id
GROUP BY kw.keyword_id, p.year
ORDER BY paper_count DESC;

-- Q4: Venue Rankings
SELECT * FROM vw_venue_stats ORDER BY avg_citations DESC;

-- Q5: Collaboration Strength
SELECT * FROM vw_collaborations ORDER BY collab_count DESC LIMIT 20;

-- Q6: Institutional Output
SELECT i.name AS institution, COUNT(DISTINCT p.paper_id) AS total_papers,
       SUM(p.citation_count_cache) AS total_citations
FROM institution i
JOIN researcher_affiliation ra ON ra.institution_id = i.institution_id
JOIN authorship a              ON a.researcher_id   = ra.researcher_id
JOIN paper p                   ON p.paper_id        = a.paper_id
WHERE p.year BETWEEN ra.start_year AND IFNULL(ra.end_year, YEAR(CURDATE()))
GROUP BY i.institution_id
ORDER BY total_citations DESC;

-- Q7: Keyword Co-occurrence
SELECT k1.term AS kw1, k2.term AS kw2,
       COUNT(*) AS co_count
FROM paper_keyword pk1
JOIN paper_keyword pk2 ON pk1.paper_id = pk2.paper_id
                       AND pk1.keyword_id < pk2.keyword_id
JOIN keyword k1 ON k1.keyword_id = pk1.keyword_id
JOIN keyword k2 ON k2.keyword_id = pk2.keyword_id
GROUP BY pk1.keyword_id, pk2.keyword_id
ORDER BY co_count DESC
LIMIT 20;

-- Q8: Full-Text Search Example
-- SELECT * FROM paper WHERE MATCH(title, abstract) AGAINST ('database systems' IN NATURAL LANGUAGE MODE);
