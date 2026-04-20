# ACADEMIC RESEARCH CITATION NETWORK SYSTEM (ARCNS)

## A Relational Database System for Scholarly Analytics

---

**Course**: Database Management Systems (DBMS)

**Submitted By**: [Team Member Names]

**Institution**: [Institution Name]

**Date**: April 2026

**Supervisor / Faculty Guide**: [Faculty Name]

---

## Table of Contents

1. [Abstract](#1-abstract)
2. [Objectives](#2-objectives)
3. [Scope](#3-scope)
4. [Schema Design](#4-schema-design)
   - 4.1 [Entity Identification](#41-entity-identification)
   - 4.2 [Relationships Between Entities](#42-relationships-between-entities)
   - 4.3 [Normalization Process](#43-normalization-process)
5. [Entity-Relationship Diagram](#5-entity-relationship-diagram)
6. [Application Overview and Screenshots](#6-application-overview-and-screenshots)
7. [SQL Query Catalog](#7-sql-query-catalog)
8. [Database Objects](#8-database-objects)
   - 8.1 [Triggers](#81-triggers)
   - 8.2 [Views](#82-views)
   - 8.3 [Stored Procedures](#83-stored-procedures)
   - 8.4 [Indexing Strategy](#84-indexing-strategy)
   - 8.5 [Transactions](#85-transactions)
9. [Tools and Technologies](#9-tools-and-technologies)
10. [Conclusion](#10-conclusion)
11. [References](#11-references)

---

## 1. Abstract

Scientific publishing has grown enormously over the past two decades — millions of new papers appear every year across journals, conferences, and workshops worldwide. For universities and research labs, tracking who published what, how often a paper gets cited, and which research topics are gaining traction has become a significant challenge. Most existing tools like Google Scholar and Semantic Scholar are proprietary, offer no SQL-level access, and do not allow institutions to maintain their own curated datasets. Manual spreadsheets, on the other hand, lack relational integrity and cannot support the kind of analytical queries researchers actually need.

The **Academic Research Citation Network System (ARCNS)** was built to address this gap. It is a relational database system designed from scratch using MySQL 8.x that models the academic publishing ecosystem — researchers, papers, venues (journals and conferences), institutions, keywords, and the citation relationships that connect them. The database stores approximately 100 researchers, 200 papers, 500+ citation links, 30 venues, 150 keywords, and 30 institutions, all generated through a controlled seeding process to simulate realistic scholarly data distributions.

Beyond just storing data, ARCNS provides meaningful analytics. It can compute the H-index for any author, trace citation chains using recursive SQL, identify keyword co-occurrence patterns, rank venues by impact factor, and surface collaboration networks between researchers. A lightweight web-based interface — a single HTML page served through a minimal Python HTTP handler — lets users run these predefined queries and view results interactively, demonstrating that the database works end-to-end without relying on any heavy application framework.

The system was developed using MySQL 8.x for the database engine, Python 3.11 with `mysql-connector-python` for the backend bridge and data generation, and plain HTML/CSS/JavaScript for the frontend. The entire focus of the project remains on sound database design principles: normalized schemas, foreign key constraints, triggers, views, stored procedures, indexed queries, and transactional integrity — all concepts central to a DBMS course.

---

## 2. Objectives

The project was driven by a set of clear objectives, each mapped to a core concept from the DBMS curriculum.

### Primary Objectives

1. **Design a Normalized Relational Schema**
   The first and most fundamental goal was to design a database schema that accurately represents the academic publishing domain. This meant identifying the right entities — Researcher, Paper, Venue, Institution, and Keyword — and the relationships between them (authorship, citation, affiliation, paper-keyword mapping). The schema had to satisfy at least Third Normal Form (3NF), and ideally Boyce-Codd Normal Form (BCNF), to eliminate redundancy and ensure data integrity.

2. **Implement Core DBMS Features on MySQL 8.x**
   The database had to go beyond simple table creation. We needed to demonstrate working knowledge of indexes (and their effect on query performance), triggers (for automated cache updates), views (for frequently used aggregated queries), stored procedures (for complex multi-step computations), and transactions (for atomic multi-table inserts). Each of these features was implemented and tested against the seed data.

3. **Develop a Catalog of Advanced SQL Queries**
   A key deliverable was a set of 10+ analytical queries that showcase different SQL features: aggregate functions with GROUP BY, window functions for H-index computation, recursive Common Table Expressions (CTEs) for citation chain traversal, self-joins for keyword co-occurrence analysis, multi-table joins for collaboration strength measurement, and full-text search using MySQL's `MATCH ... AGAINST` syntax.

4. **Build a Minimal Demonstration Interface**
   While the project's core is the database, we needed a way to show that everything works. The objective was to build a single-page HTML interface where a user can select a query from the sidebar, execute it, and see formatted results in a table. This interface is read-only and demonstration-focused — it is not intended to be a production application.

### Secondary Objectives

5. **Apply Query Optimization Techniques**
   We aimed to create strategic indexes on frequently queried columns and verify their impact using MySQL's `EXPLAIN` command, showing reductions in rows scanned and changes in access type from full table scans to index lookups.

6. **Generate Realistic Seed Data**
   The database needed to be populated with synthetic but realistic data. A Python script using the Faker library generates researchers with plausible names and ORCID identifiers, papers with titles and abstracts, citations following a power-law distribution (where a few seminal papers attract most citations), and keyword assignments drawn from computer science taxonomy.

---

## 3. Scope

### 3.1 What the System Covers (In Scope)

- **Complete ER diagram and relational schema design** covering five core entities and four relationship sets.
- **Full MySQL database implementation** with approximately 100 researchers, 200 papers, 500+ citations, 30 venues, 150 keywords, and 30 institutions.
- **All major DBMS object types**: foreign key constraints, normalization to 3NF/BCNF, secondary indexes, triggers (4 total), views (4 total), stored procedures (2 total), and transactional logic with COMMIT/ROLLBACK demonstration.
- **10+ complex SQL queries** covering diverse analytical use cases — from simple aggregations to recursive CTEs.
- **A minimal HTML/JS frontend** connected to the MySQL database through a lightweight Python HTTP handler, purely for running predefined queries and displaying results.
- **Documentation**: ER diagram, relational schema, normalization walkthrough, full query catalog, and this report.

### 3.2 What the System Does Not Cover (Out of Scope)

- **No REST API or web framework** — the system does not use Flask, Django, Express, or any API framework. The backend is a bare Python `http.server` handler.
- **No CRUD operations through the UI** — the interface is primarily demonstration-oriented. A paper insertion form exists to demonstrate transactions, but full create/read/update/delete workflows are not implemented.
- **No JavaScript frameworks** — no React, Vue, Angular, or similar frontend frameworks were used.
- **No user authentication or role-based access control** — the system runs locally and assumes a single trusted user.
- **No graph visualizations** — while citation networks lend themselves to graph visualization (D3.js, Cytoscape.js), implementing interactive graph rendering was outside the database-focused scope of this project.
- **No automated import from external APIs** — data comes from a controlled seed generator, not from live feeds like Semantic Scholar or DBLP.

### 3.3 Assumptions

- The database runs on a local MySQL 8.x instance. The user has MySQL installed and has created the `arcns` database and user credentials before running the initialization scripts.
- Seed data is synthetic and generated using Python's Faker library with a fixed random seed for reproducibility.
- Citation distributions are deliberately skewed (top 10 papers receive 20–50 citations each) to simulate the real-world power-law pattern observed in academic citation networks.
- The web interface is designed for desktop browsers and does not include mobile responsiveness.

### 3.4 Limitations

- The system is designed for demonstration and educational purposes, not for production deployment.
- Full-text search quality depends on MySQL's built-in natural language processing, which has limitations compared to dedicated search engines like Elasticsearch.
- The H-index stored procedure caches results in the `researcher` table; it needs to be explicitly re-run after new citation data is added to keep the cache current.
- The lightweight Python server is single-threaded and not suitable for concurrent multi-user access.

---

## 4. Schema Design

### 4.1 Entity Identification

After analysing the domain requirements for an academic publishing ecosystem, we identified five core entities that form the backbone of the database. Each entity was chosen because it represents a distinct real-world object with its own attributes and lifecycle.

#### Entity 1: INSTITUTION

Represents universities, research laboratories, and industrial R&D centres where researchers are affiliated.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| institution_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| name | VARCHAR(300) | NOT NULL, UNIQUE | Full institution name |
| country | VARCHAR(100) | — | Country of location |
| city | VARCHAR(100) | — | City of location |
| type | ENUM('university','lab','industry','government') | DEFAULT 'university' | Classification |

#### Entity 2: RESEARCHER

Represents individual academic authors who publish papers. Each researcher has a unique email and ORCID identifier.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| researcher_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| name | VARCHAR(200) | NOT NULL | Full name |
| email | VARCHAR(200) | UNIQUE | Contact email |
| orcid | VARCHAR(20) | UNIQUE | ORCID persistent identifier |
| h_index_cache | INT | DEFAULT 0 | Cached H-index value |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

#### Entity 3: VENUE

Represents publication venues — journals, conferences, and workshops where papers are published.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| venue_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| name | VARCHAR(300) | NOT NULL | Venue name |
| type | ENUM('journal','conference','workshop') | DEFAULT 'conference' | Venue category |
| publisher | VARCHAR(200) | — | Publishing body (ACM, IEEE, etc.) |
| impact_factor_cache | DECIMAL(6,3) | DEFAULT 0.000 | Cached average citations |

#### Entity 4: KEYWORD

Represents controlled-vocabulary terms assigned to papers for classification and search.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| keyword_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| term | VARCHAR(100) | NOT NULL, UNIQUE | Keyword text |

#### Entity 5: PAPER

The central entity of the system, representing individual academic publications.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| paper_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| title | VARCHAR(500) | NOT NULL | Paper title |
| abstract | TEXT | — | Paper abstract |
| year | YEAR | NOT NULL | Publication year |
| doi | VARCHAR(200) | UNIQUE | Digital Object Identifier |
| open_access | TINYINT(1) | DEFAULT 0 | Open access flag |
| venue_id | INT | FOREIGN KEY → venue | Where it was published |
| citation_count_cache | INT | DEFAULT 0 | Cached incoming citation count |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

The `paper` table also carries a **FULLTEXT index** on `(title, abstract)` to support natural-language search queries.

---

### 4.2 Relationships Between Entities

Apart from the five entities above, the domain requires four relationship sets to capture the connections between them. Each relationship set is implemented as a separate junction table with composite primary keys.

#### Relationship 1: AUTHORSHIP (Researcher ↔ Paper)

**Cardinality**: Many-to-Many (M:N)

A single researcher can author multiple papers, and a single paper can have multiple authors. The `author_order` field captures the sequence of authorship (first author, second author, etc.), and `is_corresponding` flags the corresponding author.

| Attribute | Data Type | Constraints |
|-----------|-----------|-------------|
| researcher_id | INT | FK → researcher, part of composite PK |
| paper_id | INT | FK → paper, part of composite PK |
| author_order | TINYINT | NOT NULL, DEFAULT 1 |
| is_corresponding | TINYINT(1) | DEFAULT 0 |

**Referential Actions**: `ON DELETE CASCADE ON UPDATE CASCADE` — if a researcher or paper is deleted, the authorship link is automatically removed.

#### Relationship 2: CITATION (Paper → Paper)

**Cardinality**: Many-to-Many, Self-Referential (M:N reflexive)

This is the most distinctive relationship in the system. A paper can cite many other papers, and a paper can be cited by many others. The relationship is directed — `citing_paper_id` references the paper that contains the citation, and `cited_paper_id` references the paper being cited. A CHECK constraint prevents a paper from citing itself.

| Attribute | Data Type | Constraints |
|-----------|-----------|-------------|
| citing_paper_id | INT | FK → paper, part of composite PK |
| cited_paper_id | INT | FK → paper, part of composite PK |
| citation_context | VARCHAR(500) | Short excerpt describing the citation |

**Integrity Rule**: `CHECK (citing_paper_id <> cited_paper_id)` — enforced both at the constraint level and through a BEFORE INSERT trigger.

#### Relationship 3: RESEARCHER_AFFILIATION (Researcher ↔ Institution)

**Cardinality**: Many-to-Many (M:N)

A researcher may be affiliated with multiple institutions over their career (e.g., PhD at one university, postdoc at another, faculty position at a third). The composite primary key includes `start_year` to allow multiple affiliations with the same institution during different time periods.

| Attribute | Data Type | Constraints |
|-----------|-----------|-------------|
| researcher_id | INT | FK → researcher, part of composite PK |
| institution_id | INT | FK → institution, part of composite PK |
| start_year | YEAR | Part of composite PK |
| end_year | YEAR | Nullable (NULL = current position) |
| role | VARCHAR(100) | e.g., 'Professor', 'PhD Student' |

#### Relationship 4: PAPER_KEYWORD (Paper ↔ Keyword)

**Cardinality**: Many-to-Many (M:N)

Each paper can be tagged with multiple keywords, and each keyword can apply to multiple papers. This simple junction table enables keyword-based search and trend analysis.

| Attribute | Data Type | Constraints |
|-----------|-----------|-------------|
| paper_id | INT | FK → paper, part of composite PK |
| keyword_id | INT | FK → keyword, part of composite PK |

#### Relationship 5: PAPER → VENUE

**Cardinality**: Many-to-One (M:1)

Each paper is published in exactly one venue, but a venue hosts many papers. This is implemented as a foreign key (`venue_id`) directly in the `paper` table rather than as a separate junction table, since the cardinality is M:1.

**Referential Action**: `ON DELETE SET NULL` — if a venue record is deleted, the paper's `venue_id` is set to NULL rather than cascading the delete to the paper itself (a paper still exists even if venue metadata is removed).

### Summary of Cardinalities

| Relationship | Type | Participating Entities | Implementation |
|-------------|------|----------------------|----------------|
| Authorship | M:N | Researcher ↔ Paper | Junction table with composite PK |
| Citation | M:N (self-ref) | Paper ↔ Paper | Junction table with CHECK constraint |
| Affiliation | M:N | Researcher ↔ Institution | Junction table with temporal PK |
| Paper-Keyword | M:N | Paper ↔ Keyword | Junction table with composite PK |
| Paper-Venue | M:1 | Paper → Venue | Foreign key in paper table |

---

### 4.3 Normalization Process

The database schema was designed following a systematic normalization process, starting from an unnormalized flat table and progressively eliminating redundancy through 1NF, 2NF, 3NF, and finally verifying BCNF compliance.

#### Step 0: The Unnormalized Starting Point

Before normalization, consider what the data might look like if it were stored naively in a single flat table — as one might find in a spreadsheet:

```
FLAT_PUBLICATION_RECORD:
  paper_id, title, abstract, year, doi,
  author1_name, author1_email, author1_orcid, author1_institution, author1_country,
  author2_name, author2_email, author2_orcid, author2_institution, author2_country,
  author3_name, author3_email, author3_orcid, author3_institution, author3_country,
  keyword1, keyword2, keyword3,
  venue_name, venue_type, venue_publisher,
  cited_paper_1, cited_paper_2, cited_paper_3, ...
```

This table has several problems:
- **Repeating groups**: author1/author2/author3 columns, keyword1/keyword2/keyword3 columns, and cited_paper columns are repeating groups with a fixed upper bound.
- **Data redundancy**: the same author's name, email, and institution are repeated across every paper they author.
- **Update anomalies**: changing an author's email requires updating every row where that author appears.
- **Insertion anomalies**: a new researcher cannot be added until they publish a paper.
- **Deletion anomalies**: deleting a researcher's only paper also loses their contact information.

#### Step 1: First Normal Form (1NF) — Eliminate Repeating Groups

**Rule**: Each cell must contain a single atomic value. No repeating groups or arrays.

**Problem identified**: The flat table stores multiple authors per row (author1, author2, author3) and multiple keywords per row (keyword1, keyword2, keyword3). These are repeating groups.

**Action taken**: We decompose the flat table into separate tables, moving the repeating groups into their own relations:

- `paper(paper_id, title, abstract, year, doi, venue_name, venue_type, venue_publisher)`
- `paper_author(paper_id, author_name, author_email, author_orcid, author_institution, author_country, author_order)`
- `paper_keyword_flat(paper_id, keyword_term)`
- `paper_citation_flat(paper_id, cited_paper_id)`

**Result**: Every cell now holds a single value. Each row in `paper_author` represents exactly one author on one paper. The schema is in **1NF**.

#### Step 2: Second Normal Form (2NF) — Eliminate Partial Dependencies

**Rule**: Every non-key attribute must depend on the **entire** composite primary key, not just part of it.

**Problem identified in `paper_author`**:
- The composite key is `(paper_id, author_name)` or more properly `(paper_id, researcher_id)`.
- `author_email` depends only on the researcher, not on which paper they wrote. That is a partial dependency: `researcher_id → author_email` (only part of the composite key determines the attribute).
- Similarly, `author_orcid`, `author_institution`, and `author_country` depend only on the researcher, not on the paper-researcher combination.

**Problem identified in `paper`**:
- `venue_name`, `venue_type`, and `venue_publisher` depend on the venue, not on the paper itself. If we think of the key as `paper_id`, these attributes actually depend on a non-key attribute (`venue_name` or an implied `venue_id`), which is a transitive dependency — but since the paper table has a simple PK, the partial dependency issue shows up differently here. We handle it in the 3NF step.

**Action taken**: Extract researcher-specific attributes into a separate `researcher` table:

- `researcher(researcher_id, name, email, orcid)`
- `authorship(researcher_id, paper_id, author_order, is_corresponding)` — only attributes that depend on the full composite key remain
- `paper_keyword(paper_id, keyword_id)` — keyword_id becomes a FK to a new `keyword` table
- `keyword(keyword_id, term)`

**Result**: In every relation with a composite key, all non-key attributes now depend on the **full** key. The schema is in **2NF**.

#### Step 3: Third Normal Form (3NF) — Eliminate Transitive Dependencies

**Rule**: No non-key attribute should depend on another non-key attribute. Equivalently, every non-key attribute must depend directly on the primary key and nothing else.

**Problem identified in `paper`**:
- The `paper` table still contains `venue_name`, `venue_type`, and `venue_publisher`.
- There is a transitive dependency chain: `paper_id → venue_name → venue_type, venue_publisher`.
- That is, the venue-related attributes depend on `venue_name` (a non-key attribute), which in turn depends on `paper_id`. This is a transitive dependency.

**Problem identified with institution data**:
- If researcher data still contained `institution_name` and `country`, there would be another transitive dependency: `researcher_id → institution_name → country`.

**Action taken**:
- Extract venue information into a dedicated `venue` table: `venue(venue_id, name, type, publisher, impact_factor_cache)`
- Add a foreign key `venue_id` in the `paper` table to reference it.
- Extract institution information into `institution(institution_id, name, country, city, type)`
- Create the `researcher_affiliation` junction table to link researchers to institutions (since a researcher can have multiple affiliations over time, this is M:N).

**Result**: Every non-key attribute in every table depends directly and solely on the primary key. No transitive dependencies remain. The schema is in **3NF**.

#### Step 4: Boyce-Codd Normal Form (BCNF) Verification

**Rule**: For every non-trivial functional dependency X → Y, X must be a superkey.

We verify BCNF compliance table by table:

| Table | Functional Dependencies | BCNF? | Reasoning |
|-------|------------------------|-------|-----------|
| institution | institution_id → name, country, city, type | ✅ | institution_id is the PK (superkey) |
| researcher | researcher_id → name, email, orcid, h_index_cache | ✅ | researcher_id is the PK |
| venue | venue_id → name, type, publisher, impact_factor_cache | ✅ | venue_id is the PK |
| keyword | keyword_id → term | ✅ | keyword_id is the PK |
| paper | paper_id → title, abstract, year, doi, venue_id, ... | ✅ | paper_id is the PK |
| authorship | (researcher_id, paper_id) → author_order, is_corresponding | ✅ | Composite PK is the determinant |
| citation | (citing_paper_id, cited_paper_id) → citation_context | ✅ | Composite PK is the determinant |
| researcher_affiliation | (researcher_id, institution_id, start_year) → end_year, role | ✅ | Composite PK is the determinant |
| paper_keyword | (paper_id, keyword_id) → ∅ (no non-key attributes) | ✅ | Trivially BCNF |

**Conclusion**: All tables satisfy BCNF. Every non-trivial functional dependency has a superkey on its left-hand side. No further decomposition is needed.

#### Normalization Summary

| Normal Form | Problem Addressed | Tables Affected |
|-------------|-------------------|-----------------|
| 1NF | Repeating groups (multiple authors/keywords per row) | Decomposed flat table into paper, paper_author, paper_keyword |
| 2NF | Partial dependencies (author email depending only on researcher_id) | Extracted researcher entity; authorship reduced to relationship attributes only |
| 3NF | Transitive dependencies (venue attributes depending on venue_name, not paper_id) | Extracted venue and institution entities |
| BCNF | Verified — no violations found | All 9 tables confirmed compliant |

---

## 5. Entity-Relationship Diagram

The ER diagram for ARCNS captures all five entities, their attributes, and the five relationships connecting them. The diagram was designed using standard ER notation with the following conventions:

- **Rectangles** represent entities
- **Ellipses** represent attributes (with underlined primary keys)
- **Diamonds** represent relationships
- **Lines** with cardinality markers (1, M, N) connect entities through relationships
- **Double lines** indicate total participation where applicable

### 5.1 ER Diagram Structure

```
    ┌──────────────┐          ┌──────────────────┐
    │ INSTITUTION  │          │    KEYWORD        │
    │──────────────│          │──────────────────│
    │ institution_id│         │ keyword_id (PK)   │
    │ name          │         │ term              │
    │ country       │         └────────┬─────────┘
    │ city          │                  │
    │ type          │                  │ M:N
    └──────┬───────┘                  │
           │                   ┌──────┴────────┐
           │ M:N               │ PAPER_KEYWORD  │
           │                   └──────┬────────┘
    ┌──────┴──────────────┐           │
    │ RESEARCHER_          │          │
    │ AFFILIATION          │   ┌──────┴─────────────────┐
    └──────┬──────────────┘   │       PAPER              │
           │                  │─────────────────────────│
    ┌──────┴───────┐          │ paper_id (PK)            │
    │ RESEARCHER   │          │ title                    │
    │──────────────│          │ abstract                 │
    │ researcher_id│   M:N    │ year                     │
    │ name         ├──────────┤ doi                      │
    │ email        │AUTHORSHIP│ open_access              │   M:1    ┌───────────┐
    │ orcid        │          │ venue_id (FK) ───────────┼─────────►│  VENUE    │
    │ h_index_cache│          │ citation_count_cache     │          │───────────│
    └──────────────┘          └──────────┬──────────────┘          │ venue_id  │
                                         │                         │ name      │
                                         │ M:N (self-referential)  │ type      │
                                         │                         │ publisher │
                                  ┌──────┴───────┐                └───────────┘
                                  │  CITATION     │
                                  │ (reflexive)   │
                                  │ citing ↔ cited│
                                  └──────────────┘
```

### 5.2 Detailed Cardinality Explanation

| Relationship Path | Cardinality | Reading |
|-------------------|-------------|---------|
| Researcher — Authorship — Paper | M : N | One researcher authors many papers; one paper has many authors |
| Paper — Citation — Paper | M : N (reflexive) | One paper cites many papers; one paper is cited by many papers |
| Researcher — Affiliation — Institution | M : N | One researcher works at many institutions over time; one institution employs many researchers |
| Paper — Paper_Keyword — Keyword | M : N | One paper has many keywords; one keyword applies to many papers |
| Paper → Venue | M : 1 | Many papers are published in one venue; a venue hosts many papers |

> **Note**: A high-resolution ER diagram should be created using a tool like Draw.io, Lucidchart, or MySQL Workbench's EER modelling feature and included below.

> **[INSERT IMAGE: ER_Diagram.png]**
> *Full Entity-Relationship diagram of the ARCNS database showing all five entities (Researcher, Paper, Venue, Institution, Keyword), their attributes, and the five relationship sets (Authorship, Citation, Affiliation, Paper_Keyword, Paper-Venue) with cardinality notations. Created using Draw.io or Lucidchart.*

---

## 6. Application Overview and Screenshots

The ARCNS application consists of three layers: the MySQL database, a lightweight Python HTTP handler that bridges the database to the browser, and a single-page HTML/CSS/JavaScript frontend.

### 6.1 System Architecture

```
┌─────────────────────────────────────────────┐
│             BROWSER (index.html)             │
│  Vanilla JS + CSS  |  Sidebar Navigation    │
│  Dashboard / Analytics / Search / Explorer   │
└───────────────────┬─────────────────────────┘
                    │  HTTP GET/POST (JSON)
┌───────────────────▼─────────────────────────┐
│          Python HTTP Handler (app.py)        │
│  http.server  |  mysql-connector-python     │
│  SQL Query Registry  |  Stored Proc Calls   │
└───────────────────┬─────────────────────────┘
                    │  SQL over TCP (port 3306)
┌───────────────────▼─────────────────────────┐
│           MySQL 8.x (arcns database)         │
│  9 Tables  |  4 Triggers  |  4 Views        │
│  2 Stored Procedures  |  5 Indexes          │
└─────────────────────────────────────────────┘
```

### 6.2 How the Backend Works

The file `app.py` implements a custom HTTP request handler by extending Python's built-in `http.server.SimpleHTTPRequestHandler`. It does not use Flask, Django, or any web framework. The handler intercepts specific URL paths and routes them to database query functions:

- **`GET /api/stats`** — Returns aggregate counts (total papers, researchers, citations, venues) for the dashboard cards.
- **`GET /api/query?type=<query_key>`** — Looks up the SQL query from an internal registry and executes it. Supports query types like `top_papers`, `author_leaderboard`, `keyword_trends`, `venue_rankings`, `collaborations`, `institutional_output`, `keyword_cooccurrence`, and `search`.
- **`GET /api/citation-chain?id=<paper_id>`** — Calls the `sp_get_citation_chain` stored procedure with a maximum depth of 3 hops.
- **`POST /api/add-paper`** — Demonstrates transactional paper insertion. Receives JSON payload, starts a transaction, inserts the paper, commits, and returns the new paper ID.

Every other request (like the root `/` path) falls through to the default handler, which serves `index.html` and other static files.

### 6.3 How the Frontend Works

The file `index.html` is a single-page application with a fixed sidebar for navigation and a main content area that switches between sections. There is no page reload — section switching is handled entirely through JavaScript DOM manipulation.

The sidebar has five navigation items:
1. **Dashboard** — Shows summary statistics (paper count, researcher count, citation count, venue count) in card format, plus a table of the top 10 most-cited publications.
2. **Analytics** — Shows the author leaderboard (ranked by total citations), venue rankings (by average citations), and institutional output (papers and citations per institution).
3. **Search Engine** — Allows the user to type a search query that runs against the paper titles and abstracts.
4. **Citation Explorer** — Accepts a paper ID and traces its citation chain using the recursive stored procedure, showing source-target-depth triples.
5. **Management** — The "Add Publication" modal allows inserting a new paper into the database, demonstrating the transactional insert capability.

### 6.4 Application Screenshots

The following screenshots demonstrate the key features of the ARCNS web interface.

---

> **[INSERT SCREENSHOT 1: Dashboard Overview]**
> *Capture the full dashboard page showing the four stat cards at the top (Total Papers, Researchers, Total Citations, Venues) and the "Top 10 Cited Publications" table below. The sidebar should be visible on the left with "Dashboard" highlighted as the active section.*

**Figure 6.1**: Dashboard Overview — The main landing page displays key database statistics as summary cards and a ranked table of the most-cited papers pulled from the `vw_top_cited_papers` view.

---

> **[INSERT SCREENSHOT 2: Analytics — Author Leaderboard]**
> *Navigate to the Analytics section and capture the Author Leaderboard table showing columns: Name, H-Index, Publications, and Citations. The sidebar should show "Analytics" as the active section.*

**Figure 6.2**: Author Leaderboard — Researchers ranked by total citations. This data is served from the `vw_author_leaderboard` database view, which joins the researcher, authorship, and paper tables and aggregates publication counts and citation sums.

---

> **[INSERT SCREENSHOT 3: Analytics — Venue Rankings and Institutional Output]**
> *Still in the Analytics section, scroll down to capture the two side-by-side cards: "Venue Rankings" (showing venue names and average citations) and "Institutional Output" (showing institution names and total citations).*

**Figure 6.3**: Venue Rankings and Institutional Output — The left card shows venues ranked by average citations per paper (from `vw_venue_stats`). The right card shows institutions ranked by total citations of their affiliated researchers, computed using a four-table join between institution, researcher_affiliation, authorship, and paper.

---

> **[INSERT SCREENSHOT 4: Search Engine]**
> *Navigate to the Search Engine section. Type a search term (e.g., "neural" or "database") in the search bar and capture the results table showing Paper ID, Title, Year, and Citations columns.*

**Figure 6.4**: Full-Text Search — The search engine sends the user's query to the backend, which runs a `LIKE` search against paper titles and abstracts. The results display matching papers with their citation counts.

---

> **[INSERT SCREENSHOT 5: Citation Chain Explorer]**
> *Navigate to the Citation Explorer section. Enter a paper ID (e.g., 5 or 10) and click "Explore Network". Capture the results table showing Source ID, Target ID, and Hops (Depth) columns with the green depth badges.*

**Figure 6.5**: Citation Chain Explorer — This feature leverages the `sp_get_citation_chain` stored procedure, which internally uses a recursive CTE to traverse the citation graph up to 3 hops deep. Each row shows a source paper, its citation target, and the traversal depth.

---

> **[INSERT SCREENSHOT 6: Add Publication Modal]**
> *Click the "+ Add Publication" button in the top-right corner and capture the modal overlay showing the form fields: Paper Title, Abstract, Year, and Venue ID, with the "Save to Database" and "Cancel" buttons.*

**Figure 6.6**: Add Publication Modal — This form demonstrates transactional paper insertion. When the user clicks "Save to Database", the frontend sends a POST request to `/api/add-paper`, which starts a MySQL transaction, inserts the paper record, and commits. If any step fails, the transaction rolls back, leaving the database unchanged.

---

## 7. SQL Query Catalog

The following queries were designed to showcase a range of SQL features and demonstrate the analytical capabilities of the ARCNS database.

### Q1: Top 10 Most-Cited Papers

**SQL Features**: LEFT JOIN, GROUP BY, ORDER BY, LIMIT, aggregate function COUNT()

```sql
SELECT p.paper_id, p.title, p.year,
       COUNT(c.citing_paper_id) AS citation_count
FROM paper p
LEFT JOIN citation c ON c.cited_paper_id = p.paper_id
GROUP BY p.paper_id
ORDER BY citation_count DESC
LIMIT 10;
```

**Purpose**: Identifies the most influential papers in the database by counting incoming citations. Uses LEFT JOIN so papers with zero citations are still included.

### Q2: Author Leaderboard

**SQL Features**: JOIN, GROUP BY, ORDER BY, COUNT(), aggregate with multiple tables

```sql
SELECT r.name, COUNT(a.paper_id) AS publications,
       r.h_index_cache
FROM researcher r
JOIN authorship a ON r.researcher_id = a.researcher_id
GROUP BY r.researcher_id
ORDER BY publications DESC
LIMIT 10;
```

**Purpose**: Ranks researchers by publication count and shows their cached H-index.

### Q3: Keyword Trends (Papers per Keyword per Year)

**SQL Features**: Three-table JOIN, GROUP BY on multiple columns, COUNT(DISTINCT)

```sql
SELECT kw.term AS keyword, p.year,
       COUNT(DISTINCT p.paper_id) AS paper_count
FROM keyword kw
JOIN paper_keyword pk ON pk.keyword_id = kw.keyword_id
JOIN paper p           ON p.paper_id   = pk.paper_id
GROUP BY kw.keyword_id, p.year
ORDER BY paper_count DESC;
```

**Purpose**: Shows how research interest in different topics has changed over time — useful for identifying emerging or declining fields.

### Q4: Collaboration Network

**SQL Features**: Self-join on authorship table, inequality join condition, COUNT(DISTINCT)

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

**Purpose**: Identifies pairs of researchers who have co-authored papers. The condition `a1.researcher_id < a2.researcher_id` prevents duplicate pairs (A-B and B-A).

### Q5: Citation Chain (Recursive CTE)

**SQL Features**: WITH RECURSIVE, Common Table Expression, UNION ALL, recursive depth tracking

```sql
WITH RECURSIVE citation_path AS (
    SELECT citing_paper_id AS source,
           cited_paper_id  AS target,
           1 AS depth
    FROM citation
    WHERE cited_paper_id = 1

    UNION ALL

    SELECT c.citing_paper_id, c.cited_paper_id, cp.depth + 1
    FROM citation c
    JOIN citation_path cp ON c.cited_paper_id = cp.source
    WHERE cp.depth < 3
)
SELECT DISTINCT source, target, depth FROM citation_path;
```

**Purpose**: Starting from a seed paper, traces all papers that cite it (depth 1), then papers that cite those citers (depth 2), and so on up to depth 3. This demonstrates MySQL 8.x's recursive CTE capability.

### Q6: Venue Impact Factor

**SQL Features**: JOIN, aggregate AVG(), ROUND(), WHERE with date function

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

**Purpose**: Ranks venues by average citations per paper (limited to the last 5 years), serving as a proxy for impact factor.

### Q7: Keyword Co-occurrence

**SQL Features**: Self-join on paper_keyword, inequality join, three-table join, GROUP BY

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

**Purpose**: Finds pairs of keywords that frequently appear on the same paper. For example, "Machine Learning" and "Neural Networks" might co-occur on 15 papers. This is a classic self-join pattern.

### Q8: Full-Text Search

**SQL Features**: MATCH...AGAINST, FULLTEXT index, natural language mode, relevance scoring

```sql
SELECT paper_id, title, year,
       MATCH(title, abstract) AGAINST ('graph neural network' IN NATURAL LANGUAGE MODE) AS relevance
FROM paper
WHERE MATCH(title, abstract) AGAINST ('graph neural network' IN NATURAL LANGUAGE MODE)
ORDER BY relevance DESC
LIMIT 20;
```

**Purpose**: Demonstrates MySQL's built-in full-text search capability. Papers are ranked by relevance to the search phrase.

### Q9: Institutional Output Ranking

**SQL Features**: Four-table JOIN, SUM(), COUNT(DISTINCT), IFNULL(), BETWEEN, date-range filtering

```sql
SELECT i.name AS institution,
       COUNT(DISTINCT p.paper_id) AS total_papers,
       SUM(p.citation_count_cache) AS total_citations
FROM institution i
JOIN researcher_affiliation ra ON ra.institution_id = i.institution_id
JOIN authorship a              ON a.researcher_id   = ra.researcher_id
JOIN paper p                   ON p.paper_id        = a.paper_id
WHERE p.year BETWEEN ra.start_year AND IFNULL(ra.end_year, YEAR(CURDATE()))
GROUP BY i.institution_id
ORDER BY total_citations DESC;
```

**Purpose**: Credits each paper to the institution(s) where its authors were affiliated during the publication year. The BETWEEN clause with IFNULL ensures that current affiliations (where end_year is NULL) are included.

---

## 8. Database Objects

### 8.1 Triggers

Four triggers were implemented to maintain data consistency and enforce business rules automatically, without requiring application-level logic.

#### Trigger 1: `trg_citation_insert` (AFTER INSERT on citation)

When a new citation is inserted, this trigger automatically increments the `citation_count_cache` of the cited paper by 1. This keeps the cached count synchronized with the actual number of citation records, avoiding the need for expensive COUNT queries every time citation data is displayed.

```sql
CREATE TRIGGER trg_citation_insert
AFTER INSERT ON citation
FOR EACH ROW
BEGIN
    UPDATE paper
    SET citation_count_cache = citation_count_cache + 1
    WHERE paper_id = NEW.cited_paper_id;
END;
```

#### Trigger 2: `trg_citation_delete` (AFTER DELETE on citation)

The complement of the insert trigger — when a citation is deleted, the cited paper's count is decremented. The `GREATEST(..., 0)` guard prevents the count from going negative in edge cases.

```sql
CREATE TRIGGER trg_citation_delete
AFTER DELETE ON citation
FOR EACH ROW
BEGIN
    UPDATE paper
    SET citation_count_cache = GREATEST(citation_count_cache - 1, 0)
    WHERE paper_id = OLD.cited_paper_id;
END;
```

#### Trigger 3: `trg_no_self_cite` (BEFORE INSERT on citation)

This trigger prevents a paper from citing itself. While a CHECK constraint (`citing_paper_id <> cited_paper_id`) also enforces this rule, the trigger provides a more descriptive error message using `SIGNAL SQLSTATE '45000'`.

```sql
CREATE TRIGGER trg_no_self_cite
BEFORE INSERT ON citation
FOR EACH ROW
BEGIN
    IF NEW.citing_paper_id = NEW.cited_paper_id THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'A paper cannot cite itself.';
    END IF;
END;
```

#### Trigger 4: `trg_refresh_venue_impact` (AFTER UPDATE on paper)

When a paper's `citation_count_cache` changes (which happens whenever triggers 1 or 2 fire), this trigger recalculates the average citations for the paper's venue and updates the venue's `impact_factor_cache`. This creates a chain of trigger actions: inserting a citation → updates paper count → updates venue average.

```sql
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
END;
```

### 8.2 Views

Four database views were created to provide pre-joined, aggregated datasets that the application queries repeatedly.

| View Name | Purpose | Tables Joined |
|-----------|---------|---------------|
| `vw_top_cited_papers` | Papers ranked by citations, with author list and venue name | paper, venue, authorship, researcher |
| `vw_author_leaderboard` | Researchers ranked by publications and citations | researcher, authorship, paper |
| `vw_venue_stats` | Venues with paper count, average citations, and max citations | venue, paper |
| `vw_collaborations` | Pairs of researchers who co-authored papers, with collaboration count | authorship (self-join), researcher |

Views simplify the application code — instead of writing complex multi-table joins every time, the backend simply runs `SELECT * FROM vw_top_cited_papers ORDER BY citations DESC LIMIT 10`.

### 8.3 Stored Procedures

Two stored procedures encapsulate complex multi-step database operations.

#### Procedure 1: `sp_calculate_h_index(IN res_id INT, OUT h_index INT)`

Computes the H-index for a given researcher and updates their cached value. The H-index is defined as the largest number *h* such that the researcher has at least *h* papers with at least *h* citations each.

The procedure uses `ROW_NUMBER() OVER (ORDER BY citation_count_cache DESC)` to rank papers by citations, then finds the maximum rank where the citation count still meets or exceeds the rank number.

#### Procedure 2: `sp_get_citation_chain(IN start_paper_id INT, IN max_depth INT)`

Uses a recursive CTE to traverse the citation graph starting from a given paper. Returns all (source, target, depth) triples up to the specified maximum depth. This procedure is called from the Citation Explorer feature in the frontend.

### 8.4 Indexing Strategy

Five secondary indexes were created to accelerate the most frequently executed queries:

| Index | Table | Column(s) | Query Accelerated |
|-------|-------|-----------|-------------------|
| `idx_citation_cited` | citation | cited_paper_id | Citation count lookups, citation chain traversal |
| `idx_paper_year` | paper | year | Keyword trends, venue impact factor (year-filtered) |
| `idx_authorship_paper` | authorship | paper_id | Author leaderboard, collaboration network |
| `idx_affil_institution` | researcher_affiliation | institution_id | Institutional output ranking |
| `idx_paper_venue` | paper | venue_id | Venue statistics queries |

In addition, the `paper` table carries a **FULLTEXT index** on `(title, abstract)` to support the `MATCH ... AGAINST` search functionality.

**EXPLAIN Analysis**: Running `EXPLAIN` before and after adding the `idx_citation_cited` index shows a significant change:
- **Before**: `type = ALL`, scanning all ~500 rows in the citation table
- **After**: `type = ref`, scanning only the matching rows (typically 2–5) for a given `cited_paper_id`

### 8.5 Transactions

The system demonstrates ACID-compliant transactional behaviour through the paper insertion workflow. When a user submits a new paper via the "Add Publication" modal:

1. The Python backend starts an explicit transaction with `conn.start_transaction()`
2. An INSERT statement adds the paper to the `paper` table
3. The `LAST_INSERT_ID()` is captured for the new paper
4. The transaction is committed with `conn.commit()`

If any step fails (for example, a duplicate DOI violates the UNIQUE constraint), the transaction rolls back automatically, leaving the database in its previous consistent state.

```sql
START TRANSACTION;

INSERT INTO paper(title, abstract, year, doi, open_access, venue_id)
VALUES ('Graph Attention Networks for Citation Analysis',
        'We propose a novel...', 2023, '10.1145/xyz', 1, 3);

SET @new_paper_id = LAST_INSERT_ID();

INSERT INTO authorship(researcher_id, paper_id, author_order, is_corresponding)
VALUES (12, @new_paper_id, 1, 1),
       (34, @new_paper_id, 2, 0);

INSERT INTO paper_keyword(paper_id, keyword_id)
  SELECT @new_paper_id, keyword_id FROM keyword
  WHERE term IN ('graph neural network','citation analysis');

INSERT INTO citation(citing_paper_id, cited_paper_id)
VALUES (@new_paper_id, 88), (@new_paper_id, 121);

COMMIT;
-- If any step above fails, ROLLBACK undoes everything
```

This guarantees **Atomicity** (all-or-nothing), **Consistency** (FK constraints and triggers are satisfied), **Isolation** (concurrent operations do not see partial data), and **Durability** (committed data survives crashes).

---

## 9. Tools and Technologies

| Category | Tool | Version | Purpose |
|----------|------|---------|---------|
| Database | MySQL | 8.x | Primary RDBMS — tables, views, triggers, stored procedures, full-text search |
| Database Tool | MySQL Workbench | 8.x | Schema design, query testing, EXPLAIN analysis |
| Backend | Python | 3.11+ | HTTP handler (`app.py`), database initialization, seed data generation |
| DB Connector | mysql-connector-python | 8.x | MySQL connection from Python code |
| Data Generation | Faker | 24.x | Synthetic researcher names, emails, paper titles, abstracts |
| Frontend | HTML + CSS + Vanilla JS | — | Single-page demonstration interface |
| Diagrams | Draw.io / Lucidchart | — | ER diagram creation |
| Version Control | Git | — | Source code management |

---

## 10. Conclusion

The Academic Research Citation Network System (ARCNS) demonstrates a complete database development lifecycle — from requirements analysis and ER modelling through normalization, schema implementation, and query engineering, all the way to a working demonstration interface.

The project covers each major topic from the DBMS curriculum in a practical, applied setting. The normalized schema (verified through 3NF and BCNF) eliminates data redundancy while preserving the richness of the academic publishing domain. The trigger system maintains cached aggregates automatically, saving expensive recomputation on every query. The views abstract away complex joins into simple, reusable query surfaces. The stored procedures encapsulate non-trivial computations (H-index, citation chain traversal) within the database layer itself. And the transactional insert workflow demonstrates the ACID guarantees that are fundamental to reliable database operation.

The analytical query catalog — spanning simple aggregations, window functions, recursive CTEs, self-joins, full-text search, and multi-table aggregations — shows that a well-designed relational database can answer sophisticated questions without any external analytics engine. The lightweight web interface ties everything together by providing an interactive way to execute these queries and inspect the results.

While ARCNS is not intended for production use, it serves its purpose as a comprehensive demonstration of relational database concepts, SQL query design, and database application development.

---

## 11. References

1. Ramakrishnan, R., & Gehrke, J. (2003). *Database Management Systems* (3rd ed.). McGraw-Hill.
2. Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). *Database System Concepts* (7th ed.). McGraw-Hill.
3. MySQL 8.0 Reference Manual. Oracle Corporation. https://dev.mysql.com/doc/refman/8.0/en/
4. Ley, M. (2009). DBLP: Some Lessons Learned. *PVLDB*, 2(2), 1493–1500.
5. Hirsch, J. E. (2005). An index to quantify an individual's scientific research output. *PNAS*, 102(46), 16569–16572.
6. Elmasri, R., & Navathe, S. B. (2015). *Fundamentals of Database Systems* (7th ed.). Pearson.

---

*Report Version 1.0 — April 2026*
*Prepared for DBMS Course Evaluation*
