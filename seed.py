"""
seed.py — Populate Neon DB with sample GTM data.
Run once: python seed.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from app.database import engine, SessionLocal
from app import models

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

COMPANIES = [
    {"company_name": "Acme Corporation",       "email": "info@acmecorp.com",          "contact": "+1 (415) 555-0101"},
    {"company_name": "Globex Industries",       "email": "sales@globex.com",           "contact": "+1 (212) 555-0134"},
    {"company_name": "Stark Enterprises",       "email": "hello@starkent.com",         "contact": "+1 (310) 555-0178"},
    {"company_name": "Initech Solutions",       "email": "contact@initech.io",         "contact": "+1 (512) 555-0192"},
    {"company_name": "Umbrella Analytics",      "email": "info@umbrella-analytics.com","contact": "+1 (628) 555-0143"},
    {"company_name": "Pied Piper Technologies", "email": "team@piedpiper.tech",        "contact": "+1 (650) 555-0167"},
    {"company_name": "Hooli Cloud",             "email": "sales@hooli.com",            "contact": "+1 (408) 555-0122"},
    {"company_name": "Dunder Mifflin Digital",  "email": "hello@dundermifflin.biz",    "contact": "+1 (570) 555-0109"},
    {"company_name": "Bluth Company",           "email": "gob@bluthcompany.com",       "contact": "+1 (949) 555-0155"},
    {"company_name": "Vandelay Industries",     "email": "art@vandelay.com",           "contact": "+1 (212) 555-0188"},
    {"company_name": "Prestige Worldwide",      "email": "info@prestigeww.com",        "contact": "+1 (305) 555-0176"},
    {"company_name": "Massive Dynamic",         "email": "walter@massivedynamic.com",  "contact": "+1 (617) 555-0131"},
    {"company_name": "Cyberdyne Systems",       "email": "sales@cyberdyne.io",         "contact": "+1 (818) 555-0114"},
    {"company_name": "Soylent Corp",            "email": "hello@soylent.co",           "contact": "+1 (323) 555-0147"},
    {"company_name": "Oscorp Technologies",     "email": "norman@oscorp.com",          "contact": "+1 (212) 555-0163"},
    {"company_name": "LexCorp",                 "email": "lex@lexcorp.com",            "contact": "+1 (312) 555-0199"},
    {"company_name": "Wayne Enterprises",       "email": "alfred@wayneenterprises.com","contact": "+1 (313) 555-0128"},
    {"company_name": "Nakatomi Trading",        "email": "info@nakatomi.jp",           "contact": "+81 3-5555-0180"},
    {"company_name": "Aperture Science",        "email": "glados@aperturescience.com", "contact": "+1 (541) 555-0102"},
    {"company_name": "Weyland-Yutani Corp",     "email": "ops@weyland-yutani.com",     "contact": "+44 20 5555 0145"},
    {"company_name": "Rekall Inc",              "email": "quaid@rekall.com",           "contact": "+1 (702) 555-0133"},
    {"company_name": "Tyrell Corporation",      "email": "eldon@tyrell.corp",          "contact": "+1 (213) 555-0171"},
    {"company_name": "BiffCo Enterprises",      "email": "biff@biffco.com",            "contact": "+1 (916) 555-0116"},
    {"company_name": "Virtucon",                "email": "info@virtucon.com",          "contact": "+1 (702) 555-0187"},
    {"company_name": "Dharma Initiative",       "email": "ben@dharma-initiative.org",  "contact": "+1 (808) 555-0139"},
]

PEOPLE = [
    {"name": "Alice Chen",       "email": "alice.chen@acmecorp.com",        "connection_strength": 9.2},
    {"name": "Bob Martinez",     "email": "bob.m@globex.com",               "connection_strength": 7.5},
    {"name": "Carol Thompson",   "email": "carol@starkent.com",             "connection_strength": 8.8},
    {"name": "David Kim",        "email": "d.kim@initech.io",               "connection_strength": 6.3},
    {"name": "Emma Wilson",      "email": "emma.w@piedpiper.tech",          "connection_strength": 9.5},
    {"name": "Frank Nguyen",     "email": "fnguyen@hooli.com",              "connection_strength": 5.7},
    {"name": "Grace Lee",        "email": "grace.lee@umbrella-analytics.com","connection_strength": 8.1},
    {"name": "Henry Park",       "email": "hpark@dundermifflin.biz",        "connection_strength": 4.9},
    {"name": "Irene Santos",     "email": "irene@bluthcompany.com",         "connection_strength": 7.2},
    {"name": "James Wright",     "email": "jwright@vandelay.com",           "connection_strength": 8.6},
    {"name": "Karen White",      "email": "kwhite@massivedynamic.com",      "connection_strength": 9.0},
    {"name": "Leo Brown",        "email": "leo.b@cyberdyne.io",             "connection_strength": 3.4},
    {"name": "Mia Davis",        "email": "mia.davis@soylent.co",           "connection_strength": 6.8},
    {"name": "Nathan Clark",     "email": "nathan@oscorp.com",              "connection_strength": 7.9},
    {"name": "Olivia Hall",      "email": "olivia.h@lexcorp.com",           "connection_strength": 5.2},
    {"name": "Peter Adams",      "email": "peter@wayneenterprises.com",     "connection_strength": 8.4},
    {"name": "Quinn Baker",      "email": "quinn@aperturescience.com",      "connection_strength": 9.1},
    {"name": "Rachel Torres",    "email": "ratorres@weyland-yutani.com",    "connection_strength": 6.6},
    {"name": "Sam Peterson",     "email": "s.peterson@rekall.com",          "connection_strength": 7.3},
    {"name": "Tara Evans",       "email": "tara.e@tyrell.corp",             "connection_strength": 8.0},
]

DEALS = [
    {"deal_name": "Acme Q1 Platform Deal",      "stage": models.DealStage.won,         "company_name": "Acme Corporation",       "value": 48000.0},
    {"deal_name": "Globex Data Pipeline",       "stage": models.DealStage.in_progress, "company_name": "Globex Industries",      "value": 72000.0},
    {"deal_name": "Stark Cloud Migration",      "stage": models.DealStage.in_progress, "company_name": "Stark Enterprises",      "value": 120000.0},
    {"deal_name": "Initech SaaS Upgrade",       "stage": models.DealStage.lead,        "company_name": "Initech Solutions",      "value": 18000.0},
    {"deal_name": "Pied Piper Compression API", "stage": models.DealStage.won,         "company_name": "Pied Piper Technologies","value": 95000.0},
    {"deal_name": "Hooli Analytics Suite",      "stage": models.DealStage.lost,        "company_name": "Hooli Cloud",            "value": 55000.0},
    {"deal_name": "Massive Dynamic Pilot",      "stage": models.DealStage.lead,        "company_name": "Massive Dynamic",        "value": 30000.0},
    {"deal_name": "Umbrella BI Rollout",        "stage": models.DealStage.in_progress, "company_name": "Umbrella Analytics",     "value": 42000.0},
    {"deal_name": "Wayne Enterprise Security",  "stage": models.DealStage.won,         "company_name": "Wayne Enterprises",      "value": 200000.0},
    {"deal_name": "Oscorp Research Tools",      "stage": models.DealStage.lead,        "company_name": "Oscorp Technologies",    "value": 25000.0},
]


def seed():
    db = SessionLocal()
    try:
        # Skip if already seeded
        if db.query(models.Company).count() > 0:
            print("Companies already seeded — skipping companies.")
        else:
            for c in COMPANIES:
                db.add(models.Company(**c))
            db.commit()
            print(f"[OK] Inserted {len(COMPANIES)} companies.")

        if db.query(models.Person).count() > 0:
            print("People already seeded - skipping people.")
        else:
            for p in PEOPLE:
                db.add(models.Person(**p))
            db.commit()
            print(f"[OK] Inserted {len(PEOPLE)} people.")

        if db.query(models.Deal).count() > 0:
            print("Deals already seeded - skipping deals.")
        else:
            for d in DEALS:
                db.add(models.Deal(**d))
            db.commit()
            print(f"[OK] Inserted {len(DEALS)} deals.")

        print("\nDone! Database seeded successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
