USE arcns;

-- ─────────────────────────────────────────────────
-- P1: Calculate H-Index for an author
-- ─────────────────────────────────────────────────
DROP PROCEDURE IF EXISTS sp_calculate_h_index;
DELIMITER $$
CREATE PROCEDURE sp_calculate_h_index(IN res_id INT, OUT h_index INT)
BEGIN
    SELECT MAX(h_val) INTO h_index
    FROM (
        SELECT citation_count_cache,
               ROW_NUMBER() OVER (ORDER BY citation_count_cache DESC) AS rk
        FROM paper p
        JOIN authorship a ON p.paper_id = a.paper_id
        WHERE a.researcher_id = res_id
    ) AS ranked
    WHERE citation_count_cache >= rk;
    
    -- Update cache
    UPDATE researcher SET h_index_cache = COALESCE(h_index, 0) WHERE researcher_id = res_id;
END$$
DELIMITER ;

-- ─────────────────────────────────────────────────
-- P2: Find Citation Chain (Recursive)
-- ─────────────────────────────────────────────────
DROP PROCEDURE IF EXISTS sp_get_citation_chain;
DELIMITER $$
CREATE PROCEDURE sp_get_citation_chain(IN start_paper_id INT, IN max_depth INT)
BEGIN
    WITH RECURSIVE citation_path AS (
        SELECT citing_paper_id AS source,
               cited_paper_id  AS target,
               1 AS depth
        FROM citation
        WHERE cited_paper_id = start_paper_id

        UNION ALL

        SELECT c.citing_paper_id, c.cited_paper_id, cp.depth + 1
        FROM citation c
        JOIN citation_path cp ON c.cited_paper_id = cp.source
        WHERE cp.depth < max_depth
    )
    SELECT DISTINCT source, target, depth FROM citation_path;
END$$
DELIMITER ;
