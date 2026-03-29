#!/usr/bin/env python3
"""Test Formatter prompt versions against existing raw audit data.

Fetches raw_data from Supabase, runs Gemini Formatter with a specific prompt version,
saves the formatted output for comparison. Costs 1 Gemini API call per run (~$0.02).

Usage:
    python3 tests/test_prompt.py                        # list available prompts
    python3 tests/test_prompt.py --prompt p0             # test p0-current prompt
    python3 tests/test_prompt.py --prompt p1 --property-id UUID
    python3 tests/test_prompt.py --compare p0 p1         # side-by-side diff

Output: tests/prompt-outputs/<prompt-version>-<property-name>.txt
"""

import argparse
import difflib
import glob
import os
import re
import sys
import time

import requests

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BACKEND_DIR)

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(BACKEND_DIR), ".env.local"))
load_dotenv(os.path.join(BACKEND_DIR, ".env"))

from google import genai
from google.genai import types

SUPABASE_URL = os.environ.get("SUPABASE_URL", os.environ.get("NEXT_PUBLIC_SUPABASE_URL", ""))
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", os.environ.get("SUPABASE_SERVICE_ROLE_KEY", ""))
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
FORMATTER_MODEL = os.environ.get("GEMINI_FORMATTER_MODEL", "gemini-3-pro-preview")

PROMPTS_DIR = os.path.join(BACKEND_DIR, "templates", "prompts")
OUTPUTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompt-outputs")
SCHEMA = "tourism_audit_v2"


def sb_get(table, params=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?{params}"
    headers = {
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "apikey": SUPABASE_KEY,
        "Accept-Profile": SCHEMA,
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()


def list_prompts():
    prompts = sorted(glob.glob(os.path.join(PROMPTS_DIR, "p*.txt")))
    if not prompts:
        print("No prompt versions found in templates/prompts/")
        return
    print(f"\nAvailable prompt versions ({len(prompts)}):")
    print("-" * 60)
    for p in prompts:
        name = os.path.basename(p).replace(".txt", "")
        size = os.path.getsize(p)
        # Read first line for description
        with open(p) as f:
            first_line = f.readline().strip()[:60]
        print(f"  {name:<25} ({size:,} bytes)  {first_line}")
    print()

    # Also list existing outputs
    outputs = sorted(glob.glob(os.path.join(OUTPUTS_DIR, "*.txt")))
    if outputs:
        print(f"Existing outputs ({len(outputs)}):")
        print("-" * 60)
        for o in outputs:
            name = os.path.basename(o).replace(".txt", "")
            size = os.path.getsize(o)
            print(f"  {name:<40} ({size:,} bytes)")
        print()


def get_raw_audit(property_id=None):
    """Fetch raw audit data + property info from DB."""
    params = "select=*&order=id.desc&limit=1"
    if property_id:
        params = f"property_id=eq.{property_id}&{params}"

    results = sb_get("audit_results", params)
    if not results:
        print("ERROR: No audit results found")
        sys.exit(1)

    audit = results[0]
    pid = audit["property_id"]

    props = sb_get("properties", f"id=eq.{pid}&select=*")
    if not props:
        print(f"ERROR: Property {pid} not found")
        sys.exit(1)

    return audit, props[0]


def load_prompt(prompt_name):
    """Load a prompt template file."""
    # Fuzzy match
    prompts = glob.glob(os.path.join(PROMPTS_DIR, f"*{prompt_name}*.txt"))
    if not prompts:
        print(f"ERROR: No prompt matching '{prompt_name}'")
        sys.exit(1)
    if len(prompts) > 1:
        print(f"Multiple matches: {[os.path.basename(p) for p in prompts]}")
        sys.exit(1)

    path = prompts[0]
    with open(path) as f:
        template = f.read()

    return os.path.basename(path).replace(".txt", ""), template


def run_formatter(prompt_text, raw_audit, prop):
    """Run Gemini Formatter with given prompt. Returns formatted text."""
    # Replace placeholders
    prompt = prompt_text.replace("{PROPERTY_NAME}", prop["property_name"])
    prompt = prompt.replace("{PROPERTY_ADDRESS}", prop.get("property_address", ""))
    prompt = prompt.replace("{WEBSITE_URL}", prop.get("website_url") or "Not available")
    prompt = prompt.replace("{RAW_AUDIT}", raw_audit)

    client = genai.Client(api_key=GOOGLE_API_KEY)

    system_instruction = (
        "You are a formatting expert. Your only task is to transform "
        "raw text into the structured Romanian template provided. "
        "Follow the structure, headings, and status icons exactly. "
        "Do not add any extra text, explanations, or markdown code blocks."
    )

    print(f"  Calling Gemini {FORMATTER_MODEL}...")
    start = time.time()

    response = client.models.generate_content(
        model=FORMATTER_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            max_output_tokens=16000,
            temperature=0.1,
        ),
    )

    elapsed = time.time() - start
    text = response.text.strip() if response.text else ""
    print(f"  Done in {elapsed:.1f}s ({len(text):,} chars)")

    return text


def test_prompt(prompt_name, property_id=None):
    """Test a prompt version against real data."""
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    audit, prop = get_raw_audit(property_id)
    prop_slug = prop["property_name"].lower().replace(" ", "-")[:30]

    print(f"Property: {prop['property_name']}")
    print(f"Raw audit: {len(audit['raw_data']):,} chars")

    prompt_version, prompt_template = load_prompt(prompt_name)
    print(f"Prompt: {prompt_version}")

    formatted = run_formatter(prompt_template, audit["raw_data"], prop)

    # Save output
    out_path = os.path.join(OUTPUTS_DIR, f"{prompt_version}--{prop_slug}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(formatted)

    print(f"\nSaved: {out_path}")
    print(f"Output: {len(formatted):,} chars")

    # Quick validation
    markers = ["AUDIT DIGITAL", "Legenda status", "1.", "2.", "3.", "Acțiuni Prioritare"]
    missing = [m for m in markers if m not in formatted]
    if missing:
        print(f"WARNING: Missing markers: {missing}")
    else:
        print("Validation: All required markers present")

    # Also generate email preview with this output
    try:
        from jinja2 import Environment, FileSystemLoader
        from src.template_processor import TemplateProcessor
        from src.models import PropertyData

        pd = PropertyData(
            property_name=prop["property_name"],
            owner_name=prop["owner_name"],
            owner_email=prop["owner_email"],
            property_address=prop.get("property_address", ""),
            website_url=prop.get("website_url", ""),
        )

        tp = TemplateProcessor.__new__(TemplateProcessor)
        tp.jinja_env = Environment(
            loader=FileSystemLoader([
                os.path.join(BACKEND_DIR, "templates"),
                os.path.join(BACKEND_DIR, "templates", "variants"),
            ]),
            autoescape=True,
        )

        html = tp.generate_html_email(formatted, pd)
        html_path = os.path.join(OUTPUTS_DIR, f"{prompt_version}--{prop_slug}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Email preview: {html_path}")
    except Exception as e:
        print(f"Email preview failed: {e}")


def compare_prompts(name1, name2):
    """Compare two prompt outputs side by side."""
    outputs1 = glob.glob(os.path.join(OUTPUTS_DIR, f"*{name1}*.txt"))
    outputs2 = glob.glob(os.path.join(OUTPUTS_DIR, f"*{name2}*.txt"))

    if not outputs1:
        print(f"No output found for '{name1}'. Run test first.")
        return
    if not outputs2:
        print(f"No output found for '{name2}'. Run test first.")
        return

    with open(outputs1[0]) as f:
        text1 = f.readlines()
    with open(outputs2[0]) as f:
        text2 = f.readlines()

    diff = list(difflib.unified_diff(
        text1, text2,
        fromfile=os.path.basename(outputs1[0]),
        tofile=os.path.basename(outputs2[0]),
        lineterm=""
    ))

    if not diff:
        print("No differences found.")
        return

    # Save diff
    diff_path = os.path.join(OUTPUTS_DIR, f"diff--{name1}-vs-{name2}.txt")
    with open(diff_path, "w") as f:
        f.write("\n".join(diff))

    print(f"Differences: {len([d for d in diff if d.startswith('+') or d.startswith('-')])} lines changed")
    print(f"Diff saved: {diff_path}")

    # Print first 50 lines
    for line in diff[:50]:
        if line.startswith("+"):
            print(f"\033[32m{line}\033[0m")
        elif line.startswith("-"):
            print(f"\033[31m{line}\033[0m")
        else:
            print(line)


def main():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("ERROR: SUPABASE_URL/SUPABASE_KEY not found")
        sys.exit(1)
    if not GOOGLE_API_KEY:
        print("ERROR: GOOGLE_API_KEY not found")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Test Formatter prompt versions")
    parser.add_argument("--prompt", "-p", help="Prompt version to test (fuzzy match)")
    parser.add_argument("--property-id", "-i", help="Property UUID (default: latest)")
    parser.add_argument("--compare", "-c", nargs=2, metavar=("V1", "V2"), help="Compare two outputs")
    args = parser.parse_args()

    if args.compare:
        compare_prompts(args.compare[0], args.compare[1])
    elif args.prompt:
        test_prompt(args.prompt, args.property_id)
    else:
        list_prompts()


if __name__ == "__main__":
    main()
