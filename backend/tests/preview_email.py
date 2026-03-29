#!/usr/bin/env python3
"""Generate email preview HTML from existing audit data in Supabase.

Usage:
    python3 tests/preview_email.py                    # ALL variants, latest audit
    python3 tests/preview_email.py --template v3      # specific variant (fuzzy match)
    python3 tests/preview_email.py --property-id UUID  # specific property
    python3 tests/preview_email.py --list              # list all properties with audits
    python3 tests/preview_email.py --variants          # list available template variants

Output: tests/previews/<variant-name>.html + index.html
"""

import argparse
import glob
import json
import os
import sys
import webbrowser

import requests

# Add backend root to path
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BACKEND_DIR)

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(BACKEND_DIR), ".env.local"))
load_dotenv(os.path.join(BACKEND_DIR, ".env"))

from jinja2 import Environment, FileSystemLoader
from src.template_processor import TemplateProcessor
from src.models import PropertyData

SUPABASE_URL = os.environ.get(
    "SUPABASE_URL", os.environ.get("NEXT_PUBLIC_SUPABASE_URL", "")
)
SUPABASE_KEY = os.environ.get(
    "SUPABASE_KEY", os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
)

TEMPLATES_DIR = os.path.join(BACKEND_DIR, "templates")
VARIANTS_DIR = os.path.join(TEMPLATES_DIR, "variants")
PREVIEWS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "previews")
SCHEMA = "tourism_audit_v2"


def sb_get(table, params=""):
    """Simple Supabase REST query."""
    url = f"{SUPABASE_URL}/rest/v1/{table}?{params}"
    headers = {
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "apikey": SUPABASE_KEY,
        "Accept-Profile": SCHEMA,
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()


def get_variant_templates():
    """Get all variant template filenames."""
    templates = sorted(glob.glob(os.path.join(VARIANTS_DIR, "v*.html")))
    return [(os.path.basename(t).replace(".html", ""), t) for t in templates]


def list_variants():
    variants = get_variant_templates()
    if not variants:
        print("No variants found in templates/variants/")
        return
    print(f"\nAvailable variants ({len(variants)}):")
    print("-" * 50)
    for name, path in variants:
        size = os.path.getsize(path)
        print(f"  {name:<30} ({size:,} bytes)")
    print()


def list_properties():
    results = sb_get("audit_results", "select=property_id")
    pids = list({r["property_id"] for r in results})
    if not pids:
        print("No audit results found.")
        return

    # Get properties one by one (simpler than IN query via REST)
    print(f"\n{'Status':>3} | {'Property Name':<35} | {'Owner':<25} | ID")
    print("-" * 110)
    for pid in pids:
        props = sb_get("properties", f"id=eq.{pid}&select=id,property_name,owner_name,status")
        for p in props:
            print(f"{p['status']:>3} | {p['property_name'][:35]:<35} | {p['owner_name'][:25]:<25} | {p['id']}")
    print()


def get_audit_data(property_id=None):
    """Fetch latest audit + property data."""
    params = "select=*&order=id.desc&limit=1"
    if property_id:
        params = f"property_id=eq.{property_id}&{params}"

    results = sb_get("audit_results", params)
    if not results:
        print(f"ERROR: No audit results found" + (f" for {property_id}" if property_id else ""))
        sys.exit(1)

    audit = results[0]
    pid = audit["property_id"]

    props = sb_get("properties", f"id=eq.{pid}&select=*")
    if not props:
        print(f"ERROR: Property {pid} not found")
        sys.exit(1)

    return audit, props[0]


def render_template(template_path, formatted_data, prop):
    """Render a Jinja2 email template with audit data."""
    pd = PropertyData(
        property_name=prop["property_name"],
        owner_name=prop["owner_name"],
        owner_email=prop["owner_email"],
        property_address=prop.get("property_address", ""),
        website_url=prop.get("website_url", ""),
    )

    tp = TemplateProcessor.__new__(TemplateProcessor)
    tp.jinja_env = Environment(
        loader=FileSystemLoader([TEMPLATES_DIR, VARIANTS_DIR]),
        autoescape=True,
    )

    audit_data_dict = tp.parse_formatted_content_to_dict(formatted_data)
    urgency_data = tp._generate_urgency_message()

    template_filename = os.path.basename(template_path)
    if "variants" in template_path:
        template_filename = f"variants/{template_filename}"

    template = tp.jinja_env.get_template(template_filename)

    return template.render(
        property_name=pd.property_name,
        audit_data=audit_data_dict,
        property_data=pd,
        meeting_link="https://calendly.com/devidevs/consultanta",
        urgency=urgency_data,
    )


def generate_previews(property_id=None, template_filter=None):
    """Generate preview HTML files for template variants."""
    os.makedirs(PREVIEWS_DIR, exist_ok=True)

    audit, prop = get_audit_data(property_id)
    print(f"Property: {prop['property_name']}")
    print(f"Owner: {prop['owner_name']}")
    print(f"Audit data: {len(audit['formatted_data']):,} chars")

    variants = get_variant_templates()
    if not variants:
        print("ERROR: No variant templates found in templates/variants/")
        sys.exit(1)

    if template_filter:
        variants = [(n, p) for n, p in variants if template_filter.lower() in n.lower()]
        if not variants:
            print(f"ERROR: No variant matching '{template_filter}'")
            sys.exit(1)

    print(f"\nGenerating {len(variants)} preview(s)...\n")

    generated = []
    for name, template_path in variants:
        try:
            html = render_template(template_path, audit["formatted_data"], prop)
            out_path = os.path.join(PREVIEWS_DIR, f"{name}.html")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"  OK  {name:<30} ({len(html):>6,} bytes)")
            generated.append(out_path)
        except Exception as e:
            print(f"  ERR {name:<30} {e}")

    print(f"\nGenerated {len(generated)}/{len(variants)} previews in tests/previews/")

    if len(generated) > 1:
        index_path = _generate_index(generated, prop["property_name"])
        print(f"Index: {index_path}")
    elif generated:
        print(f"Preview: {generated[0]}")


def _generate_index(preview_paths, property_name):
    """Generate an HTML index page linking to all previews."""
    index_path = os.path.join(PREVIEWS_DIR, "index.html")

    rows = ""
    for path in sorted(preview_paths):
        name = os.path.basename(path).replace(".html", "")
        size = os.path.getsize(path)
        # Read first line to detect theme
        with open(path) as f:
            content = f.read(2000)
        theme = "dark" if "#1E1E1E" in content else "light"
        rows += f"""
        <tr>
            <td style="padding: 12px 16px;">
                <a href="{os.path.basename(path)}" target="_blank"
                   style="color: #0D9488; text-decoration: none; font-weight: 600; font-size: 16px;">
                    {name}
                </a>
            </td>
            <td style="padding: 12px 16px; color: #6B7280; font-size: 14px;">{theme}</td>
            <td style="padding: 12px 16px; color: #6B7280; font-size: 14px;">{size:,} bytes</td>
            <td style="padding: 12px 16px;">
                <a href="{os.path.basename(path)}" target="_blank"
                   style="background: #F59E0B; color: #1F2937; padding: 6px 14px; border-radius: 6px;
                          text-decoration: none; font-size: 13px; font-weight: 600;">
                    Deschide
                </a>
            </td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Variants - {property_name}</title>
    <style>
        body {{ font-family: Inter, -apple-system, sans-serif; margin: 0; padding: 40px; background: #F8FAFC; color: #1F2937; }}
        h1 {{ font-size: 24px; margin-bottom: 4px; }}
        .sub {{ color: #6B7280; margin-bottom: 24px; font-size: 15px; }}
        table {{ width: 100%; max-width: 800px; border-collapse: collapse; background: white;
                 border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        th {{ text-align: left; padding: 12px 16px; font-size: 12px; text-transform: uppercase;
              letter-spacing: 0.05em; color: #9CA3AF; border-bottom: 1px solid #F3F4F6; }}
        tr:not(:last-child) td {{ border-bottom: 1px solid #F3F4F6; }}
        tr:hover {{ background: #F9FAFB; }}
    </style>
</head>
<body>
    <h1>Email Template Variants</h1>
    <p class="sub">Proprietate: <strong>{property_name}</strong> | {len(preview_paths)} variante | Deschide fiecare in tab nou</p>
    <table>
        <tr><th>Varianta</th><th>Theme</th><th>Size</th><th></th></tr>
        {rows}
    </table>
</body>
</html>"""

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    return index_path


def main():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("ERROR: SUPABASE_URL/SUPABASE_KEY not found in .env.local or .env")
        print("Looked for: SUPABASE_URL, NEXT_PUBLIC_SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Generate email preview from existing audit data")
    parser.add_argument("--property-id", "-p", help="Property UUID (default: latest audit)")
    parser.add_argument("--list", "-l", action="store_true", help="List properties with audits")
    parser.add_argument("--variants", "-v", action="store_true", help="List available template variants")
    parser.add_argument("--all", "-a", action="store_true", help="Generate ALL variant previews")
    parser.add_argument("--template", "-t", help="Specific variant (fuzzy match, e.g. 'v3' or 'semafor')")
    args = parser.parse_args()

    if args.variants:
        list_variants()
    elif args.list:
        list_properties()
    elif args.all or args.template:
        generate_previews(args.property_id, args.template)
    else:
        generate_previews(args.property_id)


if __name__ == "__main__":
    main()
