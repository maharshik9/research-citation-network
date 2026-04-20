# PROJECT PROPOSAL

---

**Project Title**: Academic Research Citation Network System (ARCNS) — A Relational Database System for Scholarly Analytics

**Course**: Database Management Systems (DBMS)

**Submitted By**: [Team Member Names]

**Institution**: [Institution Name]

**Date**: March 2026

**Supervisor / Faculty Guide**: [Faculty Name]

---

## Table of Contents

1. [Abstract](#1-abstract)
2. [Problem Statement](#2-problem-statement)
3. [Objectives](#3-objectives)
4. [Scope of the Project](#4-scope-of-the-project)
5. [Methodology](#5-methodology)
6. [Expected Outcomes](#6-expected-outcomes)
7. [Timeline](#7-timeline)
8. [Tools and Technologies](#8-tools-and-technologies)
9. [Team Roles and Responsibilities](#9-team-roles-and-responsibilities)
10. [References](#10-references)

---

## 1. Abstract

The exponential growth of academic literature has made it challenging to assess scholarly influence, track research trends, and identify collaboration opportunities. Existing tools are proprietary and non-customizable at the database level.

This proposal presents the **Academic Research Citation Network System (ARCNS)** — a relational database system that stores research papers, models citation relationships, tracks authorship and institutional affiliations, and provides analytical insights through advanced SQL queries. The system is accompanied by a **minimal web-based UI** (plain HTML + JavaScript) that allows users to run predefined queries and view results directly from the database — no heavy application framework involved.

ARCNS is implemented using **MySQL** as the primary database engine and a lightweight Python script (using `mysql-connector-python`) to serve a simple local HTML page. The core focus is the **database design, SQL query engineering, and DBMS feature demonstration**.

---

## 2. Problem Statement

### Background
Scientific publications are growing at millions per year. Managing citation data and deriving insight from it requires a well-designed relational database. Universities rely on citation metrics (H-index, citation count) for faculty evaluation and funding — yet most lack an in-house, transparent database system.

### Core Problem
There is no lightweight, open-source, and database-transparent system that:
- Enables institutions to maintain a curated paper and author database
- Provides SQL-level access to citation analytics
- Demonstrates the database design principles taught in a DBMS course

### Why Existing Solutions Fall Short

| Tool | Limitation |
|------|------------|
| Google Scholar | Proprietary, no SQL access |
| Semantic Scholar | Read-only API, no local ownership |
| Manual spreadsheets | No relational integrity, no analytics |

**ARCNS addresses this gap** by providing full database ownership and a transparent analytical engine built entirely on SQL.

---

## 3. Objectives

### Primary Objectives

1. **Design a normalized relational database** that accurately models the academic publishing ecosystem — entities (Researcher, Paper, Venue, Institution, Keyword) and relationships (Authorship, Citation, Affiliation, Paper-Keyword).

2. **Implement core DBMS features** — indexes, triggers, views, transactions, and stored procedures — on a MySQL 8.x instance.

3. **Demonstrate advanced SQL analytics**, including H-index calculation, citation chain traversal using Recursive CTEs, keyword co-occurrence analysis, and venue impact factor derivation.

4. **Build a minimal UI** (single HTML page + vanilla JS) that runs pre-written queries and displays results in a readable table format — purely for demonstration purposes.

### Secondary Objectives

5. **Apply query optimization** — indexing strategies verified with `EXPLAIN` output.

6. **Generate seed data** (synthetic) to populate the database and validate all queries against realistic data.

---

## 4. Scope of the Project

### In Scope
- Full ER diagram and relational schema design
- MySQL database implementation with ~100 researchers, ~200 papers, ~500 citations
- All DBMS objects: FK constraints, normalization, indexes, triggers, views, transactions
- 10+ complex SQL queries covering analytics (H-index, citation chains, keyword trends)
- Minimal HTML/JS UI to display query results (connected directly to MySQL via a lightweight Python script)
- Documentation: ER diagram, relational schema, normalization proof, query catalog, final report

### Out of Scope
- REST API or web application framework (no Flask, no Django, no Express)
- Full CRUD operations via the UI (the UI is read-only / demonstration)
- React, Vue, or any JavaScript framework on the frontend
- User authentication and role-based access control
- Mobile application development
- Graph visualizations (D3.js, Cytoscape.js — out of scope)
- Automated data import from external APIs (Semantic Scholar / DBLP)

---

## 5. Methodology

The project follows a **database-first development lifecycle** with three focused phases:

---

### Phase A — Database Design (Weeks 1–2)

**Step A1: Requirements & ER Diagram**
Define all entities, attributes, and relationships. Draw a complete ER diagram capturing:
- Five core entities: Researcher, Paper, Venue, Institution, Keyword
- Five relationship sets: Authorship (M:N), Citation (M:N self-referential), Researcher_Affiliation (M:N), Paper_Keyword (M:N), Paper-Venue (M:1)
- All attribute types: simple, composite (name → first/last), derived (citation_count), multi-valued

**Step A2: Normalization**
Begin from unnormalized flat tables and systematically apply:
- **1NF**: Eliminate repeating groups
- **2NF**: Eliminate partial functional dependencies
- **3NF**: Eliminate transitive dependencies
- **BCNF verification**: Confirm all non-trivial FDs have a superkey on the LHS

---

### Phase B — Database Implementation (Weeks 3–5)

**Step B1: DDL (Data Definition Language)**
Write `CREATE TABLE` statements for all tables with:
- Appropriate data types (INT, VARCHAR, TEXT, YEAR, ENUM, DECIMAL)
- Primary keys, composite keys, foreign keys with ON DELETE CASCADE / SET NULL
- CHECK constraints (e.g., `citing_paper_id ≠ cited_paper_id`)
- Full-text index on `paper(title, abstract)`

**Step B2: Seed Data**
Generate seed data using a Python script (Faker library) producing `INSERT` statements for:
- 100 researchers, 30 institutions, 30 venues, 150 keywords
- 200 papers, 500 citations (power-law distribution), 350 authorships

**Step B3: Advanced Database Objects**
- **Indexes**: 5 strategic indexes with before/after `EXPLAIN` analysis
- **Triggers**: citation count auto-update, self-citation prevention
- **Views**: top-cited papers, author leaderboard, venue stats, collaboration pairs
- **Transactions**: atomic paper insertion with ROLLBACK demonstration
- **Stored Procedures**: H-index calculation per author, citation chain traversal

**Step B4: SQL Query Catalog**
Write and validate 10+ analytical queries:

| Query | SQL Feature Used |
|-------|-----------------|
| Top 10 most-cited papers | GROUP BY + ORDER BY |
| H-index per author | Window functions |
| Citation chain depth | Recursive CTE |
| Keyword co-occurrence | Self-join |
| Venue impact factor | Aggregate + FK join |
| Collaboration strength | Multi-join + GROUP BY |
| Papers per year per keyword | GROUP BY + YEAR() |
| Authors with no self-citations | Subquery + NOT IN |
| Institutions by avg citation count | JOIN + AVG() |
| Full-text search on abstracts | MATCH … AGAINST |

---

### Phase C — Minimal UI & Demonstration (Weeks 6–7)

**Step C1: Minimal Python Bridge**
A single Python script (`app.py`) using `mysql-connector-python` that:
- Connects to the local MySQL instance
- Runs pre-defined SQL queries
- Serves a single-page HTML file via Python's built-in `http.server`

No Flask, no REST API — just a minimal HTTP handler to pass query results to the frontend as JSON.

**Step C2: Simple HTML/JS Frontend**
A single `index.html` file with:
- A dropdown to select which query to run
- A button to execute it
- A plain HTML `<table>` to display results
- Basic CSS for readability (no frameworks)

This UI is **demonstration-only** — its purpose is to show that the database and queries work, not to build a production application.

**Step C3: Demo Flow**
1. Select "Top 10 Cited Papers" → view results
2. Select "H-Index per Author" → view leaderboard
3. Select "Citation Chain for Paper X" → view recursive results
4. Select "Keyword Trends" → view paper counts per keyword per year
5. Trigger a transaction (insert paper) and verify trigger updated citation count

---

### Phase D — Testing & Documentation (Weeks 8–9)

**Step D1: Query Validation**
Run all 10+ queries and verify results against seed data. Use `EXPLAIN` to confirm index usage.

**Step D2: Documentation**
Produce a formal report including:
- ER diagram (draw.io)
- Relational schema (dbdiagram.io)
- Normalization walkthrough with FD proofs
- Full SQL query catalog with sample outputs
- `EXPLAIN` screenshots showing index utilization
- Trigger and view definitions with explanation
- UI screenshots from the demo

---

## 6. Expected Outcomes

### Deliverable 1 — Functional Database
A fully implemented MySQL database (`arcns_db`) containing:
- Normalized tables meeting 3NF/BCNF
- 100 researchers, 200 papers, 500+ citations (seed data)
- Triggers, views, indexes, stored procedures, and transactional logic

### Deliverable 2 — SQL Query Catalog
A documented catalog of 10+ advanced queries demonstrating analytical capabilities: H-index, citation chains, keyword co-occurrence, venue rankings, and collaboration strength.

### Deliverable 3 — Minimal Demo UI
A single HTML page (`index.html`) that connects to the database and displays query results in a table — sufficient to demonstrate that the database works end-to-end without requiring a full application stack.

### Deliverable 4 — Documentation Report
A formal DBMS course report covering all phases: ER diagrams, relational schemas, SQL listings, `EXPLAIN` output, and UI screenshots.

### Course Outcome Alignment

| Course Outcome (CO) | How ARCNS Demonstrates It |
|---------------------|---------------------------|
| CO1: Understand database concepts | ER diagram, schema, normalization |
| CO2: Write and optimize SQL | 10+ complex queries, EXPLAIN analysis |
| CO3: Design relational schemas | Full ER → relational mapping |
| CO4: Implement DB applications | Minimal UI connected to MySQL |
| CO5: Apply integrity mechanisms | Triggers, constraints, transactions |

---

## 7. Timeline

| Week | Dates (Approx.) | Milestone | Deliverable |
|------|-----------------|-----------|-------------|
| 1 | Mar 17–23 | Requirements + ER Design | ER Diagram (draw.io) |
| 2 | Mar 24–30 | Relational Schema + Normalization | schema.sql, normalization doc |
| 3 | Mar 31–Apr 6 | DDL + Seed Data | schema.sql, seed_data.sql |
| 4 | Apr 7–13 | SQL Queries + Indexes | queries.sql, EXPLAIN screenshots |
| 5 | Apr 14–20 | Triggers + Views + Transactions | triggers.sql, views.sql |
| 6 | Apr 21–27 | Stored Procedures | procedures.sql |
| 7 | Apr 28–May 4 | Minimal UI | index.html, app.py |
| 8 | May 5–11 | Testing + Bug Fixes | Verified query outputs |
| 9 | May 12–18 | Documentation + Demo Prep | Final report, demo screenshots |

---

## 8. Tools and Technologies

### Database
| Tool | Version | Purpose |
|------|---------|---------|
| MySQL | 8.x | Primary RDBMS |
| MySQL Workbench | 8.x | Schema design, query testing |

### Data Generation
| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Seed data generation script |
| Faker | 24.x | Synthetic data generation |
| mysql-connector-python | 8.x | DB connection from Python |

### Minimal UI
| Tool | Purpose |
|------|---------|
| HTML + CSS + Vanilla JS | Single-page query display interface |
| Python `http.server` | Serve the HTML file locally |

### Documentation & Diagrams
| Tool | Purpose |
|------|---------|
| draw.io / Lucidchart | ER Diagram |
| dbdiagram.io | Relational Schema visualization |
| Google Docs / Markdown | Report writing |

---

## 9. Team Roles and Responsibilities

| Role | Responsibility |
|------|----------------|
| **Database Architect** | ER design, normalization, DDL, FK constraints |
| **SQL Engineer** | Query catalog, indexes, EXPLAIN analysis |
| **DB Objects Developer** | Triggers, views, stored procedures, transactions |
| **Data & UI** | Seed data generation, minimal HTML/JS UI, Python bridge |
| **Documentation Lead** | Report writing, diagrams, demo prep |

> *Note: In smaller teams, each member will handle multiple roles. Tasks should be distributed based on phase completion goals.*

---

## 10. References

1. Ramakrishnan, R., & Gehrke, J. (2003). *Database Management Systems* (3rd ed.). McGraw-Hill.
2. Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). *Database System Concepts* (7th ed.). McGraw-Hill.
3. MySQL 8.0 Reference Manual. Oracle Corporation. https://dev.mysql.com/doc/refman/8.0/en/
4. Ley, M. (2009). DBLP: Some Lessons Learned. *PVLDB*, 2(2), 1493–1500.
5. Hirsch, J. E. (2005). An index to quantify an individual's scientific research output. *PNAS*, 102(46), 16569–16572.

---

*Proposal Version 2.0 — March 2026*
*Prepared for DBMS Course Evaluation*
