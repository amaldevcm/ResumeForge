#!/usr/bin/env python
"""Export a user's resumes from Postgres into a local JSON fixture for the
offline retrieval evaluation harness (Evaluation/scripts/run_eval.py).

Run this locally where Backend/.env's database credentials are actually
reachable - it is never imported by the offline harness itself, which has
no dependency on a live database connection.

Usage:
    python export_resumes.py --user-id <uuid> --out ../data/resumes/resumes.json
"""
import argparse
import json
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent / "Backend"
sys.path.insert(0, str(BACKEND_ROOT))

from DB import SessionLocal
from Models.Models import Document


def export_resumes(user_id, out_path):
    db = SessionLocal()
    try:
        documents = db.query(Document).filter(Document.user_id == user_id).all()
        if not documents:
            print(f"No resumes found for user_id={user_id}. Nothing written.")
            return

        records = [
            {"id": str(doc.id), "title": doc.title, "resume_text": doc.resume_text}
            for doc in documents
        ]

        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Exported {len(records)} resume(s) to {out_path}")
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Export resumes from Postgres for the eval harness.")
    parser.add_argument("--user-id", required=True,
                         help="User id to export resumes for (required even in a single-user setup, as a guard rail)")
    parser.add_argument("--out", default=None, help="Output path (default: Evaluation/data/resumes/resumes.json)")
    args = parser.parse_args()

    out_path = args.out or (Path(__file__).resolve().parent.parent / "data" / "resumes" / "resumes.json")
    export_resumes(args.user_id, out_path)


if __name__ == "__main__":
    main()
