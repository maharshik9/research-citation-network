import random
import os
from faker import Faker

fake = Faker()
Faker.seed(42)  # For reproducibility

# Configuration
NUM_INSTITUTIONS = 30
NUM_RESEARCHERS = 100
NUM_VENUES = 30
NUM_KEYWORDS = 150
NUM_PAPERS = 200
NUM_CITATIONS = 500
NUM_AUTHORSHIPS = 350
NUM_AFFILIATIONS = 120

OUTPUT_FILE = 'arcns_db/seed_data.sql'

def escape(s):
    return s.replace("'", "''")

def generate_seed_data():
    content = ["USE arcns;", "SET FOREIGN_KEY_CHECKS = 0;", "TRUNCATE TABLE authorship;", "TRUNCATE TABLE citation;", "TRUNCATE TABLE researcher_affiliation;", "TRUNCATE TABLE paper_keyword;", "TRUNCATE TABLE paper;", "TRUNCATE TABLE keyword;", "TRUNCATE TABLE venue;", "TRUNCATE TABLE researcher;", "TRUNCATE TABLE institution;", "SET FOREIGN_KEY_CHECKS = 1;", ""]

    # Institution
    types = ['university', 'lab', 'industry', 'government']
    countries = ['USA', 'UK', 'India', 'Germany', 'China', 'Canada', 'France', 'Japan', 'Switzerland', 'Singapore']
    for i in range(1, NUM_INSTITUTIONS + 1):
        name = fake.company() + " " + random.choice(['University', 'Institute', 'Labs', 'Research Center'])
        country = random.choice(countries)
        city = fake.city()
        ctype = random.choice(types)
        content.append(f"INSERT INTO institution (name, country, city, type) VALUES ('{escape(name)}', '{country}', '{city}', '{ctype}');")

    # Researcher
    for i in range(1, NUM_RESEARCHERS + 1):
        name = fake.name()
        email = fake.unique.email()
        orcid = f"{random.randint(0,9999):04d}-{random.randint(0,9999):04d}-{random.randint(0,9999):04d}-{random.randint(0,9999):04d}"
        content.append(f"INSERT INTO researcher (name, email, orcid) VALUES ('{escape(name)}', '{email}', '{orcid}');")

    # Venue
    vtypes = ['journal', 'conference', 'workshop']
    publishers = ['ACM', 'IEEE', 'Springer', 'Elsevier', 'Nature Portfolio', 'MIT Press']
    for i in range(1, NUM_VENUES + 1):
        name = fake.catch_phrase() + " " + random.choice(['Conference', 'Journal', 'Symposium', 'Workshop'])
        vtype = random.choice(vtypes)
        publisher = random.choice(publishers)
        content.append(f"INSERT INTO venue (name, type, publisher) VALUES ('{escape(name)}', '{vtype}', '{publisher}');")

    # Keyword
    topics = ['Artificial Intelligence', 'Machine Learning', 'Data Mining', 'Database Systems', 'Cloud Computing', 'Security', 'Networks', 'Software Engineering', 'HCI', 'Graphics', 'Distributed Systems', 'Blockchain', 'NLP', 'Computer Vision', 'Robotics', 'Quantum Computing', 'Bioinformatics', 'IoT', 'Cybersecurity', 'Algorithm Design']
    unique_keywords = set()
    while len(unique_keywords) < NUM_KEYWORDS:
        kw = fake.word().capitalize() + " " + random.choice(topics)
        unique_keywords.add(kw)
    
    for kw in unique_keywords:
        content.append(f"INSERT INTO keyword (term) VALUES ('{escape(kw)}');")

    # Paper
    for i in range(1, NUM_PAPERS + 1):
        title = fake.sentence(nb_words=8).rstrip('.')
        abstract = fake.paragraph(nb_sentences=5)
        year = random.randint(2010, 2024)
        doi = f"10.{random.randint(1000, 9999)}/arcns.{random.randint(10000, 99999)}"
        oa = random.choice([0, 1])
        venue_id = random.randint(1, NUM_VENUES)
        content.append(f"INSERT INTO paper (title, abstract, year, doi, open_access, venue_id) VALUES ('{escape(title)}', '{escape(abstract)}', {year}, '{doi}', {oa}, {venue_id});")

    # Authorship
    authorship_pairs = set()
    for i in range(NUM_AUTHORSHIPS):
        r_id = random.randint(1, NUM_RESEARCHERS)
        p_id = random.randint(1, NUM_PAPERS)
        if (r_id, p_id) not in authorship_pairs:
            order = random.randint(1, 5)
            is_corr = 1 if order == 1 else 0
            content.append(f"INSERT INTO authorship (researcher_id, paper_id, author_order, is_corresponding) VALUES ({r_id}, {p_id}, {order}, {is_corr});")
            authorship_pairs.add((r_id, p_id))

    # Paper_Keyword
    pk_pairs = set()
    for i in range(NUM_PAPERS * 3): # approx 3 keywords per paper
        p_id = random.randint(1, NUM_PAPERS)
        k_id = random.randint(1, NUM_KEYWORDS)
        if (p_id, k_id) not in pk_pairs:
            content.append(f"INSERT INTO paper_keyword (paper_id, keyword_id) VALUES ({p_id}, {k_id});")
            pk_pairs.add((p_id, k_id))

    # Citation
    citation_pairs = set()
    # Create some highly cited papers (power law)
    seed_papers = list(range(1, 11))
    for p_id in seed_papers:
        for _ in range(random.randint(20, 50)):
            citing_id = random.randint(1, NUM_PAPERS)
            if citing_id != p_id and (citing_id, p_id) not in citation_pairs:
                context = fake.sentence()
                content.append(f"INSERT INTO citation (citing_paper_id, cited_paper_id, citation_context) VALUES ({citing_id}, {p_id}, '{escape(context)}');")
                citation_pairs.add((citing_id, p_id))
    
    # Rest of citations
    while len(citation_pairs) < NUM_CITATIONS:
        c1 = random.randint(1, NUM_PAPERS)
        c2 = random.randint(1, NUM_PAPERS)
        if c1 != c2 and (c1, c2) not in citation_pairs:
            context = fake.sentence()
            content.append(f"INSERT INTO citation (citing_paper_id, cited_paper_id, citation_context) VALUES ({c1}, {c2}, '{escape(context)}');")
            citation_pairs.add((c1, c2))

    # Affiliation
    affil_pairs = set()
    for i in range(NUM_AFFILIATIONS):
        r_id = random.randint(1, NUM_RESEARCHERS)
        i_id = random.randint(1, NUM_INSTITUTIONS)
        start = random.randint(2005, 2020)
        end = random.choice([None, random.randint(start, 2024)])
        end_val = f"'{end}'" if end else "NULL"
        role = random.choice(['Professor', 'Assistant Professor', 'PhD Student', 'Researcher', 'Director'])
        if (r_id, i_id, start) not in affil_pairs:
            content.append(f"INSERT INTO researcher_affiliation (researcher_id, institution_id, start_year, end_year, role) VALUES ({r_id}, {i_id}, {start}, {end_val}, '{role}');")
            affil_pairs.add((r_id, i_id, start))

    # Final cache updates (since triggers are active, they will handle insert/delete)
    # But for a bulk seed, we might want to manually run the H-index sp for each researcher
    for res_id in range(1, NUM_RESEARCHERS + 1):
        content.append(f"CALL sp_calculate_h_index({res_id}, @h);")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(content))
    print(f"Seed data generated in {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_seed_data()
