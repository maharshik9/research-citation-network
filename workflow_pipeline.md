# 🎓 Academic Research Citation Network System (ARCNS)
### Full Project Pipeline & Implementation Workflow

---

> **Course Context**: DBMS Course Project — demonstrating ER Modeling, Relational Schema design, Normalization, Advanced SQL, Indexing, Triggers, Views, and Transactions.
> **Date**: March 2026 | **Target Stack**: React + Flask + MySQL

---

## 🧭 Table of Contents

1. [Project Vision & Novel Enhancements](#1-project-vision--novel-enhancements)
2. [System Architecture](#2-system-architecture)
3. [Phase 1 — Requirements Analysis](#3-phase-1--requirements-analysis)
4. [Phase 2 — ER Modeling](#4-phase-2--er-modeling)
5. [Phase 3 — Relational Schema Mapping](#5-phase-3--relational-schema-mapping)
6. [Phase 4 — Normalization](#6-phase-4--normalization)
7. [Phase 5 — Database Implementation (DDL)](#7-phase-5--database-implementation-ddl)
8. [Phase 6 — Data Population](#8-phase-6--data-population)
9. [Phase 7 — Advanced SQL Queries](#9-phase-7--advanced-sql-queries)
10. [Phase 8 — Indexing & Query Optimization](#10-phase-8--indexing--query-optimization)
11. [Phase 9 — Triggers](#11-phase-9--triggers)
12. [Phase 10 — Views](#12-phase-10--views)
13. [Phase 11 — Transactions & ACID](#13-phase-11--transactions--acid)
14. [Phase 12 — Backend API Design](#14-phase-12--backend-api-design)
15. [Phase 13 — Frontend UI Design](#15-phase-13--frontend-ui-design)
16. [Phase 14 — Visualization](#16-phase-14--visualization)
17. [Phase 15 — Testing & Verification](#17-phase-15--testing--verification)
18. [Execution Instructions](#18-execution-instructions)
19. [Project Timeline](#19-project-timeline)

---

## 1. Project Vision & Novel Enhancements

### Core Concept
The **Academic Research Citation Network System (ARCNS)** is a full-stack web application backed by a rigorously designed relational database that models the academic publishing ecosystem. Unlike a simple CRUD system, ARCNS functions as an analytical engine — letting users explore citation graphs, discover influential authors, track research trends by keyword, and understand institutional output.

### 🚀 Enhanced Ideas (Beyond the Original Brief)

| Enhancement | Description | Benefit |
|---|---|---|
| **H-Index Calculator** | Compute Hirsch index per author via SQL | Strong real-world academic metric |
| **Keyword Co-occurrence Map** | Graph showing which topics appear together most often | Demonstrates SELF-JOIN / relational analytics |
| **Citation Chain Depth** | Track how many hops away two papers are in the citation graph | Showcases recursive SQL (CTE) |
| **Venue Impact Factor** | Average citations per paper, windowed by year | Demonstrates window functions |
| **Author Collaboration Strength** | Number of co-authored papers between any two researchers | Multi-join analytics |
| **Research Trend Timeline** | Papers per keyword per year — plotted as time series | Historical scholarly trend insight |
| **Open Access Badge** | Flag papers as OA / paywalled using a boolean | Real-world relevance |
| **DOI Lookup** | Click DOI → opens paper in browser | Practical UI feature |
| **CSV / JSON Export** | Download any query result | Useful for further analysis |
| **Rate-limited REST API** | Flask-Limiter on critical endpoints | Security best practice |
| **Stored Procedures** | Wrap complex multi-step operations | Demonstrates procedural SQL |
| **Full-text Search** | `MATCH … AGAINST` on title + abstract | Demonstrates MySQL full-text indexing |

---

## 2. System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   BROWSER CLIENT                     │
│   React (Vite)  +  D3.js / Cytoscape.js             │
│   Chart.js  +  React Router  +  Axios               │
└──────────────────────┬──────────────────────────────┘
                       │  HTTP / REST (JSON)
┌──────────────────────▼──────────────────────────────┐
│                  FLASK BACKEND                       │
│   Python 3.11  |  Flask  |  Flask-CORS              │
│   Flask-Limiter  |  PyMySQL / SQLAlchemy             │
│   Marshmallow (serialization)                        │
└──────────────────────┬──────────────────────────────┘
                       │  SQL over TCP
┌──────────────────────▼──────────────────────────────┐
│                 MYSQL 8.x DATABASE                   │
│   Tables · Views · Triggers · Stored Procedures      │
│   Indexes · Transactions · Full-text Search          │
└─────────────────────────────────────────────────────┘
```

### Directory Layout

```
arcns/
├── backend/
│   ├── app.py                  # Flask entry point
│   ├── config.py               # DB credentials, config
│   ├── requirements.txt
│   ├── routes/
│   │   ├── papers.py
│   │   ├── researchers.py
│   │   ├── citations.py
│   │   ├── analytics.py
│   │   └── export.py
│   ├── db/
│   │   ├── schema.sql          # DDL
│   │   ├── seed_data.sql       # Sample data
│   │   ├── triggers.sql
│   │   ├── views.sql
│   │   └── indexes.sql
│   └── utils/
│       ├── hindex.py           # H-index computation
│       └── graph_builder.py    # Citation chain builder
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Papers.jsx
│   │   │   ├── Researchers.jsx
│   │   │   ├── CitationGraph.jsx
│   │   │   ├── Analytics.jsx
│   │   │   └── VenueStats.jsx
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── PaperCard.jsx
│   │   │   ├── AuthorCard.jsx
│   │   │   ├── CitationNetworkD3.jsx
│   │   │   ├── CollabGraph.jsx
│   │   │   └── TrendChart.jsx
│   │   └── api/
│   │       └── client.js       # Axios instance
└── docs/
    ├── ER_Diagram.png
    ├── Relational_Schema.md
    └── report.pdf
```

---

## 3. Phase 1 — Requirements Analysis

### Functional Requirements

| Module | Feature | Priority |
|---|---|---|
| Paper Management | Add / edit / delete / search papers | P0 |
| Paper Management | Attach keywords, venue, DOI | P0 |
| Author Management | Add researchers, assign institution | P0 |
| Author Management | Compute H-index, publications count | P1 |
| Citation Network | Add citations (paper → paper) | P0 |
| Citation Network | Visualize interactive graph | P1 |
| Citation Network | Citation chain depth query | P2 |
| Analytics | Leaderboards (papers, authors, venues) | P1 |
| Analytics | Keyword trend over time | P1 |
| Analytics | Collaboration network | P2 |
| Data Export | CSV / JSON export for any query | P2 |

### Non-Functional Requirements
- **Performance**: analytical queries < 2 seconds on 200 papers / 500 citations
- **Integrity**: all FK constraints enforced at DB level; no orphan records
- **Usability**: single-page application with intuitive navigation
- **Maintainability**: clear separation of backend routes, DB layer, frontend components

---

## 4. Phase 2 — ER Modeling

### Entities & Key Attributes

```
RESEARCHER
  researcher_id (PK), name, email, orcid, h_index_cache, created_at

PAPER
  paper_id (PK), title, abstract, year, doi, open_access (bool),
  venue_id (FK), citation_count_cache, created_at

VENUE
  venue_id (PK), name, type (ENUM: 'journal','conference','workshop'),
  publisher, impact_factor_cache

INSTITUTION
  institution_id (PK), name, country, city, type (ENUM: 'university','lab','industry')

KEYWORD
  keyword_id (PK), term (UNIQUE)
```

### Relationships

```
AUTHORSHIP            (RESEARCHER ↔ PAPER)   — many-to-many
  researcher_id (FK), paper_id (FK), author_order, is_corresponding

CITATION              (PAPER → PAPER)         — many-to-many self-referential
  citing_paper_id (FK), cited_paper_id (FK), citation_context

RESEARCHER_AFFILIATION (RESEARCHER ↔ INSTITUTION)
  researcher_id (FK), institution_id (FK), start_year, end_year, role

PAPER_KEYWORD         (PAPER ↔ KEYWORD)
  paper_id (FK), keyword_id (FK)
```

### Cardinalities

| Relationship | Cardinality | Notes |
|---|---|---|
| RESEARCHER — AUTHORSHIP — PAPER | M:N | A researcher authors many papers; paper has many authors |
| PAPER — CITATION — PAPER | M:N (reflexive) | A paper cites many; can be cited by many |
| RESEARCHER — RESEARCHER_AFFILIATION — INSTITUTION | M:N | Handles academic career movement |
| PAPER — PAPER_KEYWORD — KEYWORD | M:N | Controlled vocabulary |
| PAPER — VENUE | M:1 | Many papers per venue |

---

## 5. Phase 3 — Relational Schema Mapping

```sql
-- Core entities
researcher(researcher_id PK, name, email UNIQUE, orcid UNIQUE, h_index_cache, created_at)
institution(institution_id PK, name, country, city, type)
venue(venue_id PK, name, type, publisher, impact_factor_cache)
keyword(keyword_id PK, term UNIQUE)
paper(paper_id PK, title, abstract TEXT, year, doi UNIQUE, open_access,
      venue_id FK→venue, citation_count_cache, created_at)

-- Relationship tables
authorship(researcher_id FK→researcher, paper_id FK→paper,
           author_order, is_corresponding,  PK(researcher_id, paper_id))
citation(citing_paper_id FK→paper, cited_paper_id FK→paper,
         citation_context,  PK(citing_paper_id, cited_paper_id),
         CHECK citing_paper_id ≠ cited_paper_id)
researcher_affiliation(researcher_id FK→researcher, institution_id FK→institution,
                       start_year, end_year, role,
                       PK(researcher_id, institution_id, start_year))
paper_keyword(paper_id FK→paper, keyword_id FK→keyword,  PK(paper_id, keyword_id))
```

---

## 6. Phase 4 — Normalization

### 1NF — Eliminate Repeating Groups
**Before** (bad flat design):
```
Paper(paper_id, title, year, author1, author2, author3, kw1, kw2, kw3)
```
**After**: Separate `paper`, `authorship`, and `paper_keyword` tables.

### 2NF — Eliminate Partial Dependencies
In `authorship(researcher_id, paper_id, author_name)`:
- `author_name` depends only on `researcher_id`, not the full composite PK.
- **Fix**: Move `author_name` to the `researcher` table.

### 3NF — Eliminate Transitive Dependencies
In a hypothetical `paper(paper_id, venue_id, venue_name, publisher)`:
- `venue_name` and `publisher` → `venue_id`, not `paper_id` directly (transitive).
- **Fix**: Extract the `venue` entity table.

### BCNF Check
All non-trivial functional dependencies have a superkey on the left-hand side. All relationship tables use composite PKs that are themselves full determinants — BCNF is satisfied.

---

## 7. Phase 5 — Database Implementation (DDL)

```sql
CREATE DATABASE IF NOT EXISTS arcns CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE arcns;

-- ─────────────────────────────────────────────────
-- INSTITUTION
-- ─────────────────────────────────────────────────
CREATE TABLE institution (
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
CREATE TABLE researcher (
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
CREATE TABLE venue (
    venue_id            INT AUTO_INCREMENT PRIMARY KEY,
    name                VARCHAR(300) NOT NULL,
    type                ENUM('journal','conference','workshop') DEFAULT 'conference',
    publisher           VARCHAR(200),
    impact_factor_cache DECIMAL(6,3) DEFAULT 0.000
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────
-- KEYWORD
-- ─────────────────────────────────────────────────
CREATE TABLE keyword (
    keyword_id INT AUTO_INCREMENT PRIMARY KEY,
    term       VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────
-- PAPER
-- ─────────────────────────────────────────────────
CREATE TABLE paper (
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
CREATE TABLE authorship (
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
-- CITATION
-- ─────────────────────────────────────────────────
CREATE TABLE citation (
    citing_paper_id  INT NOT NULL,
    cited_paper_id   INT NOT NULL,
    citation_context VARCHAR(500),
    PRIMARY KEY (citing_paper_id, cited_paper_id),
    CONSTRAINT chk_no_self_cite CHECK (citing_paper_id <> cited_paper_id),
    FOREIGN KEY (citing_paper_id) REFERENCES paper(paper_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (cited_paper_id)  REFERENCES paper(paper_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────
-- RESEARCHER_AFFILIATION
-- ─────────────────────────────────────────────────
CREATE TABLE researcher_affiliation (
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
CREATE TABLE paper_keyword (
    paper_id   INT NOT NULL,
    keyword_id INT NOT NULL,
    PRIMARY KEY (paper_id, keyword_id),
    FOREIGN KEY (paper_id)   REFERENCES paper(paper_id)   ON DELETE CASCADE,
    FOREIGN KEY (keyword_id) REFERENCES keyword(keyword_id) ON DELETE CASCADE
) ENGINE=InnoDB;
```

---

## 8. Phase 6 — Data Population

### Strategy
- **100 researchers** — varied names, institutions (MIT, Stanford, IIT Delhi, Cambridge, ETH Zurich, etc.)
- **200 papers** — spanning years 2010–2024, covering AI, databases, systems, algorithms
- **500+ citations** — biased toward highly cited "seed" papers to simulate real citation distributions (power law)
- **30 venues** — major conferences (NeurIPS, VLDB, ICSE, SIGMOD) and journals (TODS, CACM)
- **150 keywords** — drawn from ACM CCS taxonomy

### Seed Script Approach
The `seed_data.sql` file uses:
- Faker-generated Python script to emit SQL `INSERT` statements
- Citation edges added so that the top 10 papers each have 50+ citations (Pareto distribution)
- At least 20 collaboration pairs

### Python Seed Generator Snippet
```python
from faker import Faker
import random, textwrap

fake = Faker()
institutions = ["MIT","Stanford","IIT Delhi","Cambridge","ETH Zurich",
                "Carnegie Mellon","Oxford","NUS","EPFL","TU Berlin"]

for i in range(1, 101):
    name  = fake.name()
    email = fake.unique.email()
    orcid = f"0000-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"
    print(f"INSERT INTO researcher(name,email,orcid) VALUES('{name}','{email}','{orcid}');")
```

---

## 9. Phase 7 — Advanced SQL Queries

### Q1 — Most Cited Papers (Top 10)
```sql
SELECT p.paper_id, p.title, p.year,
       COUNT(c.citing_paper_id) AS citation_count
FROM paper p
LEFT JOIN citation c ON c.cited_paper_id = p.paper_id
GROUP BY p.paper_id
ORDER BY citation_count DESC
LIMIT 10;
```

### Q2 — Most Productive Authors
```sql
SELECT r.name, COUNT(a.paper_id) AS publications,
       r.h_index_cache
FROM researcher r
JOIN authorship a ON r.researcher_id = a.researcher_id
GROUP BY r.researcher_id
ORDER BY publications DESC
LIMIT 10;
```

### Q3 — H-Index Calculation (Pure SQL)
```sql
-- For researcher_id = 42
SELECT MAX(h_val) AS h_index FROM (
    SELECT p.paper_id,
           p.citation_count_cache,
           RANK() OVER (ORDER BY p.citation_count_cache DESC) AS rk,
           COUNT(*) OVER () AS total_papers
    FROM paper p
    JOIN authorship a ON a.paper_id = p.paper_id
    WHERE a.researcher_id = 42
) ranked
WHERE citation_count_cache >= rk AS h_val
-- simplified: use application-layer computation for full accuracy
;
```

### Q4 — Collaboration Network (Authors Who Co-Authored)
```sql
SELECT r1.name AS author_a, r2.name AS author_b,
       COUNT(DISTINCT a1.paper_id) AS shared_papers
FROM authorship a1
JOIN authorship a2  ON a1.paper_id = a2.paper_id
                   AND a1.researcher_id < a2.researcher_id
JOIN researcher r1  ON r1.researcher_id = a1.researcher_id
JOIN researcher r2  ON r2.researcher_id = a2.researcher_id
GROUP BY a1.researcher_id, a2.researcher_id
HAVING shared_papers >= 1
ORDER BY shared_papers DESC;
```

### Q5 — Citation Chain (Recursive CTE — 2-hop)
```sql
WITH RECURSIVE citation_path AS (
    -- Base: direct citations of seed paper
    SELECT citing_paper_id AS source,
           cited_paper_id  AS target,
           1 AS depth
    FROM citation
    WHERE cited_paper_id = 1          -- seed paper_id

    UNION ALL

    -- Recursive: papers that cite the citers
    SELECT c.citing_paper_id, c.cited_paper_id, cp.depth + 1
    FROM citation c
    JOIN citation_path cp ON c.cited_paper_id = cp.source
    WHERE cp.depth < 3
)
SELECT DISTINCT source, target, depth FROM citation_path;
```

### Q6 — Keyword Research Trend (Papers per Keyword per Year)
```sql
SELECT kw.term AS keyword, p.year,
       COUNT(DISTINCT p.paper_id) AS paper_count
FROM keyword kw
JOIN paper_keyword pk ON pk.keyword_id = kw.keyword_id
JOIN paper p           ON p.paper_id   = pk.paper_id
GROUP BY kw.keyword_id, p.year
ORDER BY kw.term, p.year;
```

### Q7 — Venue Impact Factor (avg citations, last 5 years)
```sql
SELECT v.name, v.type,
       ROUND(AVG(p.citation_count_cache), 2) AS avg_citations,
       COUNT(p.paper_id) AS total_papers
FROM venue v
JOIN paper p ON p.venue_id = v.venue_id
WHERE p.year >= YEAR(CURDATE()) - 5
GROUP BY v.venue_id
ORDER BY avg_citations DESC;
```

### Q8 — Full-Text Search on Title + Abstract
```sql
SELECT paper_id, title, year,
       MATCH(title, abstract) AGAINST ('graph neural network' IN NATURAL LANGUAGE MODE) AS relevance
FROM paper
WHERE MATCH(title, abstract) AGAINST ('graph neural network' IN NATURAL LANGUAGE MODE)
ORDER BY relevance DESC
LIMIT 20;
```

### Q9 — Institutional Output Ranking
```sql
SELECT i.name AS institution, COUNT(DISTINCT p.paper_id) AS total_papers,
       SUM(p.citation_count_cache) AS total_citations
FROM institution i
JOIN researcher_affiliation ra ON ra.institution_id = i.institution_id
JOIN authorship a              ON a.researcher_id   = ra.researcher_id
JOIN paper p                   ON p.paper_id        = a.paper_id
WHERE p.year BETWEEN ra.start_year AND IFNULL(ra.end_year, YEAR(CURDATE()))
GROUP BY i.institution_id
ORDER BY total_citations DESC;
```

### Q10 — Keyword Co-occurrence
```sql
SELECT k1.term AS kw1, k2.term AS kw2,
       COUNT(*) AS co_count
FROM paper_keyword pk1
JOIN paper_keyword pk2 ON pk1.paper_id = pk2.paper_id
                       AND pk1.keyword_id < pk2.keyword_id
JOIN keyword k1 ON k1.keyword_id = pk1.keyword_id
JOIN keyword k2 ON k2.keyword_id = pk2.keyword_id
GROUP BY pk1.keyword_id, pk2.keyword_id
ORDER BY co_count DESC
LIMIT 30;
```

---

## 10. Phase 8 — Indexing & Query Optimization

```sql
-- Speed up citation lookups by cited paper
CREATE INDEX idx_citation_cited   ON citation(cited_paper_id);

-- Speed up paper lookups by year (used in trend queries)
CREATE INDEX idx_paper_year       ON paper(year);

-- Speed up authorship resolution by paper
CREATE INDEX idx_authorship_paper ON authorship(paper_id);

-- Speed up affiliation joins
CREATE INDEX idx_affil_institution ON researcher_affiliation(institution_id);

-- Speed up paper searches by venue
CREATE INDEX idx_paper_venue      ON paper(venue_id);
```

### EXPLAIN Analysis
Run `EXPLAIN SELECT …` before and after adding indexes to demonstrate:
- `rows` scanned reduced from ~200 to <10
- `type` changes from `ALL` (full scan) to `ref` or `range`

```sql
-- Before index:
EXPLAIN SELECT * FROM citation WHERE cited_paper_id = 5;
-- After index: type = 'ref', rows = ~3 instead of 500
```

---

## 11. Phase 9 — Triggers

### T1 — Auto-increment citation count on insert
```sql
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
```

### T2 — Auto-decrement citation count on delete
```sql
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
```

### T3 — Prevent self-citation (Application-layer safety net)
```sql
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
```

### T4 — Refresh venue impact factor cache
```sql
DELIMITER $$
CREATE TRIGGER trg_refresh_venue_impact
AFTER UPDATE ON paper
FOR EACH ROW
BEGIN
    IF OLD.citation_count_cache <> NEW.citation_count_cache THEN
        UPDATE venue v
        SET impact_factor_cache = (
            SELECT AVG(p.citation_count_cache)
            FROM paper p WHERE p.venue_id = v.venue_id
        )
        WHERE v.venue_id = NEW.venue_id;
    END IF;
END$$
DELIMITER ;
```

---

## 12. Phase 10 — Views

```sql
-- V1: Top cited papers with author list
CREATE OR REPLACE VIEW vw_top_cited_papers AS
SELECT p.paper_id, p.title, p.year, p.doi,
       v.name AS venue,
       p.citation_count_cache AS citations,
       GROUP_CONCAT(r.name ORDER BY a.author_order SEPARATOR ', ') AS authors
FROM paper p
LEFT JOIN venue     v  ON v.venue_id     = p.venue_id
LEFT JOIN authorship a  ON a.paper_id     = p.paper_id
LEFT JOIN researcher r  ON r.researcher_id = a.researcher_id
GROUP BY p.paper_id
ORDER BY citations DESC;

-- V2: Author leaderboard
CREATE OR REPLACE VIEW vw_author_leaderboard AS
SELECT r.researcher_id, r.name, r.email, r.h_index_cache,
       COUNT(DISTINCT a.paper_id) AS total_publications,
       SUM(p.citation_count_cache) AS total_citations
FROM researcher r
JOIN authorship a ON a.researcher_id = r.researcher_id
JOIN paper p      ON p.paper_id = a.paper_id
GROUP BY r.researcher_id;

-- V3: Venue statistics
CREATE OR REPLACE VIEW vw_venue_stats AS
SELECT v.venue_id, v.name, v.type,
       COUNT(p.paper_id)               AS total_papers,
       ROUND(AVG(p.citation_count_cache),2) AS avg_citations,
       MAX(p.citation_count_cache)     AS max_citations
FROM venue v
LEFT JOIN paper p ON p.venue_id = v.venue_id
GROUP BY v.venue_id;

-- V4: Collaboration pairs
CREATE OR REPLACE VIEW vw_collaborations AS
SELECT r1.researcher_id AS author_a_id, r1.name AS author_a,
       r2.researcher_id AS author_b_id, r2.name AS author_b,
       COUNT(DISTINCT a1.paper_id) AS collab_count
FROM authorship a1
JOIN authorship a2  ON a1.paper_id = a2.paper_id AND a1.researcher_id < a2.researcher_id
JOIN researcher r1  ON r1.researcher_id = a1.researcher_id
JOIN researcher r2  ON r2.researcher_id = a2.researcher_id
GROUP BY a1.researcher_id, a2.researcher_id;
```

---

## 13. Phase 11 — Transactions & ACID

### Scenario: Adding a New Paper (Atomic multi-table insert)
```sql
START TRANSACTION;

-- Step 1: Insert paper
INSERT INTO paper(title, abstract, year, doi, open_access, venue_id)
VALUES ('Graph Attention Networks for Citation Analysis',
        'We propose a novel...', 2023, '10.1145/xyz', 1, 3);

SET @new_paper_id = LAST_INSERT_ID();

-- Step 2: Link authors (order matters)
INSERT INTO authorship(researcher_id, paper_id, author_order, is_corresponding)
VALUES (12, @new_paper_id, 1, 1),
       (34, @new_paper_id, 2, 0),
       (7,  @new_paper_id, 3, 0);

-- Step 3: Attach keywords
INSERT IGNORE INTO keyword(term) VALUES ('graph neural network'), ('citation analysis');
INSERT INTO paper_keyword(paper_id, keyword_id)
  SELECT @new_paper_id, keyword_id FROM keyword
  WHERE term IN ('graph neural network','citation analysis');

-- Step 4: Add outgoing citations
INSERT INTO citation(citing_paper_id, cited_paper_id)
VALUES (@new_paper_id, 88), (@new_paper_id, 121), (@new_paper_id, 55);

COMMIT;
-- ROLLBACK; -- uncomment to demonstrate rollback on error
```

**ACID Guarantee**: If any step fails (e.g., bad foreign key), `ROLLBACK` leaves the database unchanged — no partial paper entry.

---

## 14. Phase 12 — Backend API Design

### Flask Route Map

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/papers` | List papers (paginated, filterable by year/venue/keyword) |
| POST | `/api/papers` | Add new paper (transactional) |
| GET | `/api/papers/<id>` | Paper detail + authors + citations |
| GET | `/api/papers/search?q=` | Full-text search |
| GET | `/api/researchers` | List researchers (sorted by publications/citations) |
| POST | `/api/researchers` | Add researcher |
| GET | `/api/researchers/<id>` | Author profile + H-index + papers |
| GET | `/api/citations/graph?paper_id=` | Ego-network for D3 visualization |
| GET | `/api/analytics/top_papers` | Top cited papers |
| GET | `/api/analytics/top_authors` | Author leaderboard |
| GET | `/api/analytics/venues` | Venue statistics |
| GET | `/api/analytics/trends?keyword=` | Papers per year for a keyword |
| GET | `/api/analytics/collaborations` | Collaboration edge list |
| GET | `/api/export/csv?table=` | CSV export |

### Sample Flask Route
```python
@app.route('/api/papers', methods=['GET'])
@limiter.limit("60 per minute")
def get_papers():
    page  = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    year  = request.args.get('year', None, type=int)
    q     = request.args.get('q', None)

    sql = "SELECT * FROM vw_top_cited_papers"
    filters, params = [], []
    if year:
        filters.append("year = %s"); params.append(year)
    if q:
        filters.append("MATCH(title, abstract) AGAINST (%s IN NATURAL LANGUAGE MODE)")
        params.append(q)
    if filters:
        sql += " WHERE " + " AND ".join(filters)
    sql += f" LIMIT %s OFFSET %s"
    params += [limit, (page-1)*limit]

    with get_db() as cur:
        cur.execute(sql, params)
        results = cur.fetchall()
    return jsonify(results)
```

---

## 15. Phase 13 — Frontend UI Design

### Pages & Components

| Page | Key Components | Data Source |
|------|----------------|-------------|
| **Home** | Stats banner, recent papers, search bar | `/api/analytics/top_papers`, `/api/papers` |
| **Search Papers** | Filter sidebar, paper cards, pagination | `/api/papers`, `/api/papers/search` |
| **Paper Detail** | Metadata, authors, cite-in / cited-by lists | `/api/papers/<id>` |
| **Author Profile** | Stats (H-index, pubs, citations), paper list | `/api/researchers/<id>` |
| **Citation Graph** | D3 force-directed network (interactive) | `/api/citations/graph` |
| **Analytics** | Charts: top papers, trends, venue stats | `/api/analytics/*` |
| **Collaboration** | Cytoscape.js bipartite author graph | `/api/analytics/collaborations` |

### Design System
- **Font**: Inter (Google Fonts)
- **Palette**: Deep navy `#0d1b2a`, accent teal `#00c9a7`, warm amber `#f7c59f`
- **Card style**: Glassmorphism with `backdrop-filter: blur(12px)`
- **Animations**: Framer Motion page transitions; hover lift on cards

---

## 16. Phase 14 — Visualization

### Citation Network (D3.js Force-Directed)
```javascript
const simulation = d3.forceSimulation(nodes)
    .force("link",    d3.forceLink(links).id(d => d.id).distance(80))
    .force("charge",  d3.forceManyBody().strength(-200))
    .force("center",  d3.forceCenter(width/2, height/2))
    .force("collide", d3.forceCollide(20));

// Node size = citation count (log scale)
node.attr("r", d => Math.max(6, Math.log(d.citations + 1) * 5));
```

### Keyword Trend (Chart.js Line)
```javascript
new Chart(ctx, {
    type: 'line',
    data: { labels: years, datasets: keywords.map(kw => ({
        label: kw.term,
        data: kw.counts,
        tension: 0.4
    }))},
    options: { responsive: true, plugins: { legend: { position: 'bottom' }}}
});
```

### Collaboration Graph (Cytoscape.js)
- Nodes = authors; edges = co-authorship count (thickness = weight)
- Community detection via greedy modularity coloring (client-side)

---

## 17. Phase 15 — Testing & Verification

### Backend Tests (pytest)
```bash
cd backend
pytest tests/ -v --tb=short
```

| Test | Assertion |
|------|-----------|
| `test_paper_insert` | POST returns 201, paper visible in GET |
| `test_citation_trigger` | Insert citation → `citation_count_cache` increments |
| `test_self_citation_blocked` | Insert same paper as citer and cited → 400 error |
| `test_transaction_rollback` | Incomplete transaction → no partial data |
| `test_fulltext_search` | Query returns ranked results |

### SQL Verification
```sql
-- Verify trigger worked
SELECT citation_count_cache FROM paper WHERE paper_id = 1;

-- Verify view accuracy
SELECT * FROM vw_author_leaderboard LIMIT 5;

-- EXPLAIN to confirm index usage
EXPLAIN SELECT * FROM citation WHERE cited_paper_id = 1;
```

---

## 18. Execution Instructions

### Prerequisites
```
MySQL 8.x    (with root access)
Python 3.11+
Node.js 18+
```

### Step 1 — Database Setup
```bash
mysql -u root -p < backend/db/schema.sql
mysql -u root -p arcns < backend/db/seed_data.sql
mysql -u root -p arcns < backend/db/triggers.sql
mysql -u root -p arcns < backend/db/views.sql
mysql -u root -p arcns < backend/db/indexes.sql
```

### Step 2 — Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python app.py                  # Runs on http://localhost:5000
```

### Step 3 — Frontend
```bash
cd frontend
npm install
npm run dev                    # Runs on http://localhost:5173
```

### Step 4 — Access
Open `http://localhost:5173` in your browser.

---

## 19. Project Timeline

| Week | Phase | Deliverable |
|------|-------|-------------|
| 1 | Requirements + ER Design | ER Diagram, entity list |
| 2 | Schema + Normalization | schema.sql, normalization report |
| 3 | DDL + Seed Data | schema.sql, seed_data.sql |
| 4 | SQL Queries + Indexes | queries.sql, EXPLAIN screenshots |
| 5 | Triggers + Views + Transactions | triggers.sql, views.sql |
| 6 | Backend API | Flask server, all endpoints live |
| 7 | Frontend UI | All pages working, connected to API |
| 8 | Visualization | D3 / Cytoscape graphs live |
| 9 | Testing + Refinement | Test results, fixed bugs |
| 10 | Documentation + Demo | Final report, demo video |

---

*Document prepared: March 2026*
*System: Academic Research Citation Network System (ARCNS)*
