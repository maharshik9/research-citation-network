USE arcns;

-- ─────────────────────────────────────────────────
-- T1: Auto-increment citation count on insert
-- ─────────────────────────────────────────────────
DROP TRIGGER IF EXISTS trg_citation_insert;
DELIMITER $$
CREATE TRIGGER trg_citation_insert
AFTER INSERT ON citation
FOR EACH ROW
BEGIN
    UPDATE paper
    SET citation_count_cache = citation_count_cache + 1
    WHERE paper_id = NEW.cited_paper_id;
END$$
DELIMITER ;

-- ─────────────────────────────────────────────────
-- T2: Auto-decrement citation count on delete
-- ─────────────────────────────────────────────────
DROP TRIGGER IF EXISTS trg_citation_delete;
DELIMITER $$
CREATE TRIGGER trg_citation_delete
AFTER DELETE ON citation
FOR EACH ROW
BEGIN
    UPDATE paper
    SET citation_count_cache = GREATEST(citation_count_cache - 1, 0)
    WHERE paper_id = OLD.cited_paper_id;
END$$
DELIMITER ;

-- ─────────────────────────────────────────────────
-- T3: Prevent self-citation
-- ─────────────────────────────────────────────────
DROP TRIGGER IF EXISTS trg_no_self_cite;
DELIMITER $$
CREATE TRIGGER trg_no_self_cite
BEFORE INSERT ON citation
FOR EACH ROW
BEGIN
    IF NEW.citing_paper_id = NEW.cited_paper_id THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'A paper cannot cite itself.';
    END IF;
END$$
DELIMITER ;

-- ─────────────────────────────────────────────────
-- T4: Refresh venue impact factor cache
-- ─────────────────────────────────────────────────
DROP TRIGGER IF EXISTS trg_refresh_venue_impact;
DELIMITER $$
CREATE TRIGGER trg_refresh_venue_impact
AFTER UPDATE ON paper
FOR EACH ROW
BEGIN
    IF OLD.citation_count_cache <> NEW.citation_count_cache THEN
        UPDATE venue v
        SET impact_factor_cache = (
            SELECT COALESCE(AVG(p.citation_count_cache), 0)
            FROM paper p WHERE p.venue_id = v.venue_id
        )
        WHERE v.venue_id = NEW.venue_id;
    END IF;
END$$
DELIMITER ;
