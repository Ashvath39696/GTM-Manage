"""
seed_large.py — Generate ~10k synthetic GTM records in Neon.
  Companies : 2,000
  People    : 5,000
  Deals     : 3,000

Usage:
  python seed_large.py           # adds on top of existing data
  python seed_large.py --reset   # truncates tables first, then seeds
"""

import sys
import os
import uuid
import random
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import text
from app.database import engine, SessionLocal
from app import models

# ── Word banks ────────────────────────────────────────────────────────────────

ADJECTIVES = [
    "Accel", "Adaptive", "Advanced", "Agile", "Alpha", "Apex", "Arc", "Arch",
    "Ascend", "Atomic", "Aurora", "Avant", "Azure", "Beacon", "Blue", "Bold",
    "Bright", "Broad", "Carbon", "Cardinal", "Catalyst", "Cedar", "Centric",
    "Chrome", "Cipher", "Clarity", "Clear", "Cloud", "Cobalt", "Cognito",
    "Coherent", "Collective", "Core", "Crest", "Crisp", "Cross", "Crown",
    "Crystal", "Cyber", "Dart", "Deep", "Delta", "Digital", "Direct", "Distinct",
    "Distributed", "Diverse", "Domain", "Durable", "Dynamic", "Edge", "Elastic",
    "Electric", "Elite", "Ember", "Emerge", "Empower", "Enterprise", "Epic",
    "Equal", "Equinox", "Evo", "Exact", "Exec", "Expand", "Expert", "Extreme",
    "Fathom", "Fiber", "Field", "First", "Flex", "Flow", "Fluid", "Focal",
    "Forge", "Forward", "Fusion", "Future", "Galactic", "Genesis", "Global",
    "Gold", "Grand", "Granite", "Green", "Grid", "Growth", "Harbor", "Helix",
    "High", "Horizon", "Hub", "Hyper", "Impact", "Index", "Infra", "Innov",
    "Insight", "Instinct", "Integrated", "Intel", "Invent", "Iron", "Keystone",
    "Kinetic", "Laser", "Launch", "Layer", "Lead", "Legacy", "Level", "Light",
    "Link", "Lunar", "Macro", "Magnet", "Managed", "Matrix", "Maxim", "Measure",
    "Medial", "Mentor", "Meta", "Micro", "Mint", "Mirror", "Mission", "Momentum",
    "Motion", "Multi", "Nano", "Native", "Navigate", "Neo", "Net", "Neural",
    "Nexus", "North", "Nova", "Omni", "Open", "Orbit", "Origin", "Pacific",
    "Parallax", "Peak", "Pilot", "Pioneer", "Pivot", "Pixel", "Platform",
    "Polar", "Portal", "Precise", "Premier", "Prime", "Prism", "Proton",
    "Provident", "Pulse", "Quantum", "Radius", "Rapid", "Real", "Relay",
    "Renew", "Resolve", "Rise", "Robust", "Root", "Scale", "Secure", "Sharp",
    "Signal", "Silver", "Simple", "Smart", "Solar", "Solid", "Source", "Spark",
    "Spectrum", "Sprint", "Square", "Star", "Stellar", "Sterling", "Strategic",
    "Stream", "Summit", "Swift", "Sync", "Synapse", "Synergy", "Tactile",
    "Talent", "Teal", "Terra", "Titan", "Toggle", "Total", "Transform",
    "Transparent", "Trend", "Unified", "Unity", "Universal", "Upward", "Urban",
    "Vantage", "Vector", "Venture", "Verge", "Vertex", "Vista", "Vital",
    "Vivid", "Volt", "Wave", "Wide", "Wire", "Zenith", "Zero", "Zeta",
]

NOUNS = [
    "AI", "Analytics", "API", "App", "Arc", "Arch", "Automation", "Base",
    "Bridge", "Builder", "Capital", "Chain", "Cloud", "Code", "Collective",
    "Commerce", "Connect", "Core", "Data", "Delivery", "Design", "Dev",
    "Dynamics", "Edge", "Engine", "Exchange", "Finance", "Flow", "Force",
    "Forge", "Framework", "Frontier", "Fuel", "Gateway", "Graph", "Grid",
    "Growth", "Hub", "Index", "Industries", "Infra", "Insight", "Intelligence",
    "IO", "IQ", "Key", "Lab", "Labs", "Layer", "Ledger", "Link", "Logic",
    "Loop", "Market", "Media", "Mind", "Mint", "Minds", "Mobile", "Networks",
    "Node", "Ops", "Orbit", "Path", "Pipeline", "Platform", "Portal", "Protocol",
    "Reach", "Relay", "Scale", "SDK", "Search", "Shield", "Signal", "Software",
    "Solutions", "Source", "Space", "Stack", "Stream", "Studio", "Suite",
    "Supply", "Systems", "Team", "Tech", "Tools", "Track", "Trade", "Trust",
    "Vector", "Ventures", "Vision", "Works", "World",
]

SUFFIXES = [
    "Inc", "LLC", "Ltd", "Co", "Corp", "Group", "Holdings", "Technologies",
    "Enterprises", "Partners", "Associates", "Global", "International",
]

FIRST_NAMES = [
    "Aaron", "Abby", "Adam", "Aisha", "Alex", "Alexis", "Alice", "Alicia",
    "Alison", "Amanda", "Amber", "Amy", "Ana", "Andrea", "Andrew", "Angela",
    "Anna", "Anthony", "Aria", "Ashley", "Austin", "Ava", "Benjamin", "Beth",
    "Blake", "Brandon", "Brianna", "Brittany", "Brooklyn", "Bryan", "Caleb",
    "Carlos", "Carol", "Caroline", "Carter", "Catherine", "Charles", "Charlotte",
    "Chelsea", "Chris", "Christina", "Christine", "Christopher", "Claire",
    "Cody", "Colin", "Connor", "Crystal", "Dakota", "Daniel", "Daniela",
    "David", "Devin", "Diana", "Diego", "Dylan", "Eduardo", "Elena", "Elijah",
    "Elizabeth", "Ella", "Emily", "Emma", "Eric", "Ethan", "Eva", "Evan",
    "Faith", "Fiona", "Frank", "Gabriel", "Gary", "George", "Grace", "Hannah",
    "Harper", "Henry", "Isabella", "Jacob", "Jade", "Jake", "James", "Jason",
    "Jennifer", "Jessica", "John", "Jonathan", "Jordan", "Joseph", "Joshua",
    "Julia", "Julian", "Justin", "Karen", "Katherine", "Kayla", "Kevin",
    "Kimberly", "Laura", "Lauren", "Leah", "Leon", "Lily", "Lisa", "Logan",
    "Lucas", "Luis", "Madison", "Marcus", "Maria", "Mark", "Mason", "Matthew",
    "Maya", "Megan", "Michael", "Michelle", "Miguel", "Mia", "Monica", "Nathan",
    "Nicholas", "Nicole", "Noah", "Nora", "Olivia", "Omar", "Oscar", "Patrick",
    "Paul", "Peter", "Rachel", "Rebecca", "Richard", "Riley", "Robert", "Ryan",
    "Samantha", "Samuel", "Sandra", "Sara", "Sarah", "Scott", "Sean", "Sophia",
    "Stephanie", "Steven", "Taylor", "Thomas", "Timothy", "Tyler", "Victoria",
    "Vincent", "William", "Zoe",
]

LAST_NAMES = [
    "Adams", "Allen", "Anderson", "Baker", "Barnes", "Bell", "Bennett",
    "Brooks", "Brown", "Butler", "Campbell", "Carter", "Chen", "Clark",
    "Collins", "Cook", "Cooper", "Cox", "Cruz", "Davis", "Diaz", "Edwards",
    "Evans", "Fisher", "Flores", "Foster", "Garcia", "Gonzalez", "Green",
    "Griffin", "Hall", "Harris", "Hernandez", "Hill", "Howard", "Hughes",
    "Jackson", "James", "Jenkins", "Johnson", "Jones", "Jordan", "Kelly",
    "Kim", "King", "Kumar", "Lee", "Lewis", "Liu", "Long", "Lopez", "Martin",
    "Martinez", "Miller", "Mitchell", "Moore", "Morgan", "Morris", "Murphy",
    "Nelson", "Nguyen", "Patel", "Patterson", "Perez", "Perry", "Peterson",
    "Phillips", "Powell", "Price", "Ramirez", "Reed", "Richardson", "Rivera",
    "Roberts", "Robinson", "Rodriguez", "Rogers", "Ross", "Russell", "Sanchez",
    "Sanders", "Scott", "Sharma", "Smith", "Stewart", "Sullivan", "Taylor",
    "Thomas", "Thompson", "Torres", "Turner", "Walker", "Ward", "Washington",
    "Watson", "White", "Williams", "Wilson", "Wood", "Wright", "Young", "Zhang",
]

DEAL_TYPES = [
    "Platform License", "Annual Contract", "Enterprise Deal", "Pilot Program",
    "Expansion Deal", "Renewal", "Professional Services", "Integration Contract",
    "SaaS Subscription", "Consulting Package", "Support Contract", "API Access",
    "Data Package", "Growth Package", "Strategic Partnership", "Proof of Concept",
    "Managed Services", "Custom Build", "Migration Project", "Audit & Advisory",
]

AREA_CODES = [
    "201", "212", "213", "214", "215", "216", "303", "305", "312", "313",
    "404", "407", "408", "415", "424", "469", "503", "512", "516", "617",
    "628", "646", "650", "702", "713", "720", "737", "818", "857", "929",
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def gen_uuid():
    return str(uuid.uuid4())


def rand_phone():
    area = random.choice(AREA_CODES)
    mid = random.randint(200, 999)
    end = random.randint(1000, 9999)
    return f"+1 ({area}) {mid}-{end}"


def rand_datetime_past(days=730):
    """Random UTC datetime within the past `days` days."""
    offset = timedelta(
        days=random.randint(0, days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    return datetime.now(timezone.utc) - offset


def slugify(name: str) -> str:
    return name.lower().replace(" ", "-").replace(",", "").replace(".", "")


# ── Generators ────────────────────────────────────────────────────────────────

def generate_companies(n: int) -> list[dict]:
    seen = set()
    companies = []
    while len(companies) < n:
        adj  = random.choice(ADJECTIVES)
        noun = random.choice(NOUNS)
        sfx  = random.choice(SUFFIXES)
        name = f"{adj} {noun} {sfx}"
        if name in seen:
            # disambiguate with a number
            name = f"{adj} {noun} {random.randint(2, 99)} {sfx}"
        seen.add(name)
        slug = slugify(f"{adj}{noun}")
        companies.append({
            "id":           gen_uuid(),
            "company_name": name,
            "email":        f"info@{slug}.com",
            "contact":      rand_phone(),
        })
    return companies


def generate_people(n: int, company_names: list[str]) -> list[dict]:
    people = []
    domains = ["gmail.com", "outlook.com", "yahoo.com", "company.io",
               "workmail.com", "proton.me", "corp.net"]
    for _ in range(n):
        first = random.choice(FIRST_NAMES)
        last  = random.choice(LAST_NAMES)
        domain = random.choice(domains)
        suffix = random.randint(1, 99) if random.random() < 0.3 else ""
        email = f"{first.lower()}.{last.lower()}{suffix}@{domain}"
        people.append({
            "id":                      gen_uuid(),
            "name":                    f"{first} {last}",
            "email":                   email,
            "connection_strength":     round(random.uniform(0.0, 10.0), 1),
            "last_email_interaction":  rand_datetime_past(365) if random.random() > 0.2 else None,
            "last_calendar_interaction": rand_datetime_past(180) if random.random() > 0.4 else None,
        })
    return people


def generate_deals(n: int, company_names: list[str]) -> list[dict]:
    stages = [s.value for s in models.DealStage]
    stage_weights = [0.35, 0.30, 0.25, 0.10]   # lead, in_progress, won, lost
    deals = []
    for _ in range(n):
        company = random.choice(company_names)
        deal_type = random.choice(DEAL_TYPES)
        stage = random.choices(stages, weights=stage_weights)[0]
        # Won deals tend to be larger; leads tend to be smaller
        if stage == "won":
            value = round(random.uniform(20_000, 500_000), 2)
        elif stage == "lost":
            value = round(random.uniform(5_000, 150_000), 2)
        else:
            value = round(random.uniform(5_000, 300_000), 2)
        deals.append({
            "id":           gen_uuid(),
            "deal_name":    f"{company.split()[0]} {deal_type}",
            "stage":        stage,
            "company_name": company,
            "value":        value,
        })
    return deals


# ── Main ──────────────────────────────────────────────────────────────────────

def bulk_insert(table, rows: list[dict], batch_size=500):
    """Insert rows in batches using SQLAlchemy core for speed."""
    with engine.begin() as conn:
        for i in range(0, len(rows), batch_size):
            conn.execute(table.__table__.insert(), rows[i:i + batch_size])
    return len(rows)


def seed(reset=False):
    models.Base.metadata.create_all(bind=engine)

    if reset:
        print("Resetting tables...")
        with engine.begin() as conn:
            conn.execute(text("TRUNCATE TABLE deals, people, companies RESTART IDENTITY CASCADE"))
        print("Tables truncated.")

    db = SessionLocal()
    try:
        existing_companies = db.query(models.Company).count()
        existing_people    = db.query(models.Person).count()
        existing_deals     = db.query(models.Deal).count()
    finally:
        db.close()

    # ── Companies ─────────────────────────────────────────────────────────────
    target_companies = 2000
    to_add_companies = max(0, target_companies - existing_companies)
    company_names = []

    if to_add_companies == 0:
        print(f"Companies already at {existing_companies} - skipping.")
        db2 = SessionLocal()
        try:
            company_names = [r.company_name for r in db2.query(models.Company.company_name).all()]
        finally:
            db2.close()
    else:
        print(f"Generating {to_add_companies} companies...", flush=True)
        companies = generate_companies(to_add_companies)
        company_names = [c["company_name"] for c in companies]
        n = bulk_insert(models.Company, companies)
        print(f"[OK] Inserted {n} companies (total target: {target_companies}).")

    # ── People ────────────────────────────────────────────────────────────────
    target_people = 5000
    to_add_people = max(0, target_people - existing_people)

    if to_add_people == 0:
        print(f"People already at {existing_people} - skipping.")
    else:
        print(f"Generating {to_add_people} people...", flush=True)
        people = generate_people(to_add_people, company_names)
        n = bulk_insert(models.Person, people)
        print(f"[OK] Inserted {n} people (total target: {target_people}).")

    # ── Deals ─────────────────────────────────────────────────────────────────
    target_deals = 3000
    to_add_deals = max(0, target_deals - existing_deals)

    if to_add_deals == 0:
        print(f"Deals already at {existing_deals} - skipping.")
    else:
        if not company_names:
            db3 = SessionLocal()
            try:
                company_names = [r.company_name for r in db3.query(models.Company.company_name).all()]
            finally:
                db3.close()
        print(f"Generating {to_add_deals} deals...", flush=True)
        deals = generate_deals(to_add_deals, company_names)
        n = bulk_insert(models.Deal, deals)
        print(f"[OK] Inserted {n} deals (total target: {target_deals}).")

    print("\nDone! Final counts:")
    db_final = SessionLocal()
    try:
        print(f"  Companies : {db_final.query(models.Company).count()}")
        print(f"  People    : {db_final.query(models.Person).count()}")
        print(f"  Deals     : {db_final.query(models.Deal).count()}")
    finally:
        db_final.close()


if __name__ == "__main__":
    reset = "--reset" in sys.argv
    if reset:
        confirm = input("This will DELETE all existing data. Type 'yes' to confirm: ")
        if confirm.strip().lower() != "yes":
            print("Aborted.")
            sys.exit(0)
    seed(reset=reset)
