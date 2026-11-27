#!/usr/bin/env python3
"""
Crawl all interview questions from app.bigocoding.com/interviews
WITHOUT consuming any AI practice round quota.

How it works:
- POST /api/interviews/sessions with mode="SINGLE_ROUND" fetches question content
  with aiInterviewEnabled=False → zero AI quota consumed.
- All question content (title, description, examples, constraints, starter code)
  is returned in the session response.

Usage:
  python3 crawl_bigocoding.py --token <JWT_TOKEN> --out output/
"""

import argparse
import json
import os
import time
import urllib.request
import urllib.error

BASE_URL = "https://app.bigocoding.com"

def api_get(token, path):
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        headers={"x-auth-token": token}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def api_post(token, path, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=data,
        headers={"x-auth-token": token, "Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read()), None
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return None, f"HTTP {e.code}: {body[:200]}"

def get_companies(token):
    return api_get(token, "/api/interviews/companies")

def get_blueprint(token, company_slug):
    return api_get(token, f"/api/interviews/companies/{company_slug}/blueprint")

def fetch_round_questions(token, blueprint_id, round_id):
    """
    Fetch questions for a specific round WITHOUT consuming AI quota.
    mode=SINGLE_ROUND + targetRoundId → aiInterviewEnabled=False
    """
    payload = {
        "blueprintId": blueprint_id,
        "mode": "SINGLE_ROUND",
        "targetRoundId": round_id,
    }
    data, err = api_post(token, "/api/interviews/sessions", payload)
    if err:
        return None, err
    session_rounds = data.get("sessionRounds", [])
    if not session_rounds:
        return None, "no sessionRounds in response"
    sr = session_rounds[0]
    # NOTE: aiInterviewEnabled=True is fine — quota is only consumed when you
    # actually START an AI conversation (POST .../technical-interview endpoint).
    # SINGLE_ROUND just fetches questions; it does NOT consume quota.
    return sr, None

def extract_problems(session_round):
    problems = []
    for p in session_round.get("problems", []):
        prob = p.get("problem", {})
        problems.append({
            "id": prob.get("id"),
            "code": prob.get("code"),
            "title": prob.get("title"),
            "title_en": prob.get("title_en"),
            "difficulty": prob.get("difficulty"),
            "description": prob.get("description", ""),
            "description_en": prob.get("description_en", ""),
            "starter_code": prob.get("starter_code", {}),
            "function_signature": prob.get("function_signature", {}),
        })
    return problems

def crawl(token, out_dir, company_filter=None, delay=0.5):
    os.makedirs(out_dir, exist_ok=True)

    print("Fetching company list...")
    companies = get_companies(token)
    print(f"Found {len(companies)} companies.\n")

    all_data = {}
    total_questions = 0
    skipped_rounds = 0

    for company in companies:
        slug = company["slug"]
        name = company["name"]

        if company_filter and slug not in company_filter:
            continue

        print(f"── {name} ({slug})")
        try:
            bp_data = get_blueprint(token, slug)
        except Exception as e:
            print(f"  ✗ Failed to get blueprint: {e}")
            continue

        blueprints = bp_data.get("blueprints", [])
        company_data = {
            "slug": slug,
            "name": name,
            "category": company.get("category"),
            "blueprints": []
        }

        for bp in blueprints:
            bp_id = bp["id"]
            bp_slug = bp["slug"]
            bp_role = bp.get("role", "")
            bp_level = bp.get("level", "")
            rounds = bp.get("rounds", [])

            print(f"  [{bp_slug}] {bp_role} ({bp_level}) — {len(rounds)} rounds")

            bp_entry = {
                "id": bp_id,
                "slug": bp_slug,
                "role": bp_role,
                "level": bp_level,
                "rounds": []
            }

            for rnd in rounds:
                round_id = rnd["id"]
                round_name = rnd.get("name", "")
                round_type = rnd.get("type", "")
                problem_count = rnd.get("problemCount", 0)

                if problem_count == 0:
                    bp_entry["rounds"].append({
                        "id": round_id,
                        "name": round_name,
                        "type": round_type,
                        "problems": []
                    })
                    continue

                print(f"    {round_name} ({round_type}, {problem_count} problems)", end=" ... ", flush=True)
                session_round, err = fetch_round_questions(token, bp_id, round_id)
                time.sleep(delay)

                if session_round is None:
                    print(f"✗ {err}")
                    skipped_rounds += 1
                    bp_entry["rounds"].append({
                        "id": round_id,
                        "name": round_name,
                        "type": round_type,
                        "problems": [],
                        "error": str(err)
                    })
                    continue

                problems = extract_problems(session_round)
                total_questions += len(problems)
                print(f"✓ {len(problems)} questions")

                bp_entry["rounds"].append({
                    "id": round_id,
                    "name": round_name,
                    "type": round_type,
                    "problems": problems
                })

            company_data["blueprints"].append(bp_entry)

        all_data[slug] = company_data

        # Save per-company file
        company_file = os.path.join(out_dir, f"{slug}.json")
        with open(company_file, "w", encoding="utf-8") as f:
            json.dump(company_data, f, ensure_ascii=False, indent=2)
        print(f"  → Saved: {company_file}\n")

    # Save combined file
    combined_file = os.path.join(out_dir, "all_questions.json")
    with open(combined_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"{'='*55}")
    print(f"✅  Done!")
    print(f"   Total questions crawled : {total_questions}")
    print(f"   Skipped rounds          : {skipped_rounds}")
    print(f"   Output directory        : {out_dir}/")
    print(f"   Combined file           : {combined_file}")
    print(f"\n⚠️  AI quota consumed: 0  (aiInterviewEnabled=False)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl BigOCoding interview questions")
    parser.add_argument("--token", required=True, help="JWT token (x-auth-token)")
    parser.add_argument("--out", default="bigocoding_questions", help="Output directory")
    parser.add_argument("--companies", nargs="+", help="Filter by company slugs e.g. --companies google meta")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between API calls (seconds)")
    args = parser.parse_args()

    crawl(
        token=args.token,
        out_dir=args.out,
        company_filter=set(args.companies) if args.companies else None,
        delay=args.delay,
    )
