CREATE DATABASE IF NOT EXISTS arcns CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE arcns;

-- ─────────────────────────────────────────────────
-- INSTITUTION
-- ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS institution (
    institution_id INT AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(300) NOT NULL,
    country        VARCHAR(100),
    city           VARCHAR(100),
    type           ENUM('university','lab','industry','government') DEFAULT 'university',
    UNIQUE KEY uq_institution_name (name)
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────
-- RESEARCHER
-- ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS researcher (
    researcher_id  INT AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(200) NOT NULL,
    email          VARCHAR(200) UNIQUE,
    orcid          VARCHAR(20)  UNIQUE,
    h_index_cache  INT DEFAULT 0,
    created_at     DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────
-- VENUE
-- ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS venue (
    venue_id            INT AUTO_INCREMENT PRIMARY KEY,
    name                VARCHAR(300) NOT NULL,
    type                ENUM('journal','conference','workshop') DEFAULT 'conference',
    publisher           VARCHAR(200),
    impact_factor_cache DECIMAL(6,3) DEFAULT 0.000
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────
-- KEYWORD
-- ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS keyword (
    keyword_id INT AUTO_INCREMENT PRIMARY KEY,
    term       VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────
-- PAPER
-- ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS paper (
    paper_id            INT AUTO_INCREMENT PRIMARY KEY,
    title               VARCHAR(500) NOT NULL,
    abstract            TEXT,
    year                YEAR NOT NULL,
    doi                 VARCHAR(200) UNIQUE,
    open_access         TINYINT(1) DEFAULT 0,
    venue_id            INT,
    citation_count_cache INT DEFAULT 0,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    FULLTEXT KEY ft_paper_title_abstract (title, abstract),
    FOREIGN KEY (venue_id) REFERENCES venue(venue_id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────
-- AUTHORSHIP
-- ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS authorship (
    researcher_id    INT NOT NULL,
    paper_id         INT NOT NULL,
    author_order     TINYINT NOT NULL DEFAULT 1,
    is_corresponding TINYINT(1) DEFAULT 0,
    PRIMARY KEY (researcher_id, paper_id),
    FOREIGN KEY (researcher_id) REFERENCES researcher(researcher_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (paper_id)     REFERENCES paper(paper_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────
-- CITATION (FIXED)
-- ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS citation (
    citing_paper_id  INT NOT NULL,
    cited_paper_id   INT NOT NULL,
    citation_context VARCHAR(500),
    PRIMARY KEY (citing_paper_id, cited_paper_id),
    FOREIGN KEY (citing_paper_id) REFERENCES paper(paper_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (cited_paper_id)  REFERENCES paper(paper_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────
-- RESEARCHER_AFFILIATION
-- ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS researcher_affiliation (
    researcher_id  INT NOT NULL,
    institution_id INT NOT NULL,
    start_year     YEAR NOT NULL,
    end_year       YEAR,
    role           VARCHAR(100),
    PRIMARY KEY (researcher_id, institution_id, start_year),
    FOREIGN KEY (researcher_id)  REFERENCES researcher(researcher_id)
        ON DELETE CASCADE,
    FOREIGN KEY (institution_id) REFERENCES institution(institution_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────
-- PAPER_KEYWORD
-- ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS paper_keyword (
    paper_id   INT NOT NULL,
    keyword_id INT NOT NULL,
    PRIMARY KEY (paper_id, keyword_id),
    FOREIGN KEY (paper_id)   REFERENCES paper(paper_id)   ON DELETE CASCADE,
    FOREIGN KEY (keyword_id) REFERENCES keyword(keyword_id) ON DELETE CASCADE
) ENGINE=InnoDB;
