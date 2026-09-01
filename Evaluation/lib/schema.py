"""Load and validate the eval test set and resume fixtures."""
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TestCase:
    id: str
    jd_text: str
    correct_resume_ids: list
    job_title: str = ""
    company: str = ""
    notes: str = ""
    labeled_date: str = ""


@dataclass
class Resume:
    id: str
    title: str
    resume_text: str


def load_testset(path):
    path = Path(path)
    cases = []
    seen_ids = set()
    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"{path}:{line_num}: invalid JSON - {e}")

            case_id = data.get("id")
            if not case_id:
                raise ValueError(f"{path}:{line_num}: missing required field 'id'")
            if case_id in seen_ids:
                raise ValueError(f"{path}:{line_num}: duplicate id '{case_id}'")
            seen_ids.add(case_id)

            jd_text = data.get("jd_text")
            if not jd_text:
                raise ValueError(f"{path}:{line_num}: missing required field 'jd_text' for id '{case_id}'")

            correct_resume_ids = data.get("correct_resume_ids")
            if not correct_resume_ids or not isinstance(correct_resume_ids, list):
                raise ValueError(
                    f"{path}:{line_num}: 'correct_resume_ids' must be a non-empty list for id '{case_id}'"
                )

            cases.append(TestCase(
                id=case_id,
                jd_text=jd_text,
                correct_resume_ids=correct_resume_ids,
                job_title=data.get("job_title", ""),
                company=data.get("company", ""),
                notes=data.get("notes", ""),
                labeled_date=data.get("labeled_date", ""),
            ))

    if not cases:
        raise ValueError(f"{path}: test set is empty")
    return cases


def load_resumes(path):
    path = Path(path)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list) or not data:
        raise ValueError(f"{path}: expected a non-empty JSON array of resumes")

    resumes = []
    seen_ids = set()
    for i, entry in enumerate(data):
        resume_id = entry.get("id")
        if not resume_id:
            raise ValueError(f"{path}[{i}]: missing required field 'id'")
        if resume_id in seen_ids:
            raise ValueError(f"{path}[{i}]: duplicate resume id '{resume_id}'")
        seen_ids.add(resume_id)

        resume_text = entry.get("resume_text")
        if not resume_text:
            raise ValueError(f"{path}[{i}]: missing required field 'resume_text' for id '{resume_id}'")

        resumes.append(Resume(
            id=resume_id,
            title=entry.get("title", resume_id),
            resume_text=resume_text,
        ))

    return resumes


def validate_testset_against_resumes(cases, resumes):
    """Cross-check that every correct_resume_id actually exists in the
    resume fixture. A missing reference is a data-integrity bug (e.g. a
    stale id after re-exporting resumes) - exclude the affected case from
    scoring rather than silently letting it count as an unrecoverable miss,
    and report the exclusion loudly rather than hiding it.

    Returns (valid_cases, excluded_case_ids).
    """
    resume_ids = {r.id for r in resumes}
    valid_cases = []
    excluded_case_ids = []
    for case in cases:
        missing = [rid for rid in case.correct_resume_ids if rid not in resume_ids]
        if missing:
            print(
                f"WARNING: test case '{case.id}' references unknown resume id(s) {missing} "
                "- excluding from evaluation. Re-run export_resumes.py or fix the test set."
            )
            excluded_case_ids.append(case.id)
        else:
            valid_cases.append(case)
    return valid_cases, excluded_case_ids
