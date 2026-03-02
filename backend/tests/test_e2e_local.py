#!/usr/bin/env python3
"""End-to-end local test — skips Gemini Deep Research (30-90 min),
tests everything else with LIVE Supabase + Resend.

What this tests:
  1. Insert property into live Supabase
  2. Mark as running (status 1)
  3. Insert raw audit result (from example file)
  4. Template processing via Gemini (real API call, ~10 sec)
  5. Generate PDF (fpdf2)
  6. Send REAL email via Resend (with PDF attachment)
  7. Update status to success (99)
  8. Verify audit_logs recorded everything

Usage:
    cd backend
    source .venv/bin/activate
    python tests/test_e2e_local.py

WARNING: This sends a REAL email to the test address!
"""

import sys
import os
import logging

# Setup
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load env vars from .env.local (parent dir)
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env.local")
load_dotenv(env_path)

# Map env vars that backend expects
if not os.environ.get("SUPABASE_URL"):
    os.environ["SUPABASE_URL"] = os.environ.get("NEXT_PUBLIC_SUPABASE_URL", "")
if not os.environ.get("SUPABASE_KEY"):
    os.environ["SUPABASE_KEY"] = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger("e2e_test")

from src.models import PropertyData
from src.database_service import SupabaseService
from src.template_processor import TemplateProcessor
from src.pdf_generator import generate_audit_pdf
from src.email_service import EmailService
from config import MEETING_LINK


def main():
    # ── Config ───────────────────────────────────────────────
    # Send test email to owner (judocky21) — change if needed
    TEST_EMAIL = "judocky21@gmail.com"

    print("=" * 60)
    print("END-TO-END LOCAL TEST")
    print("=" * 60)
    print(f"Target email: {TEST_EMAIL}")
    print(f"Meeting link: {MEETING_LINK}")
    print()

    # ── Load example audit ───────────────────────────────────
    example_path = os.path.join(os.path.dirname(__file__), "example_audit_output.txt")
    with open(example_path, "r", encoding="utf-8") as f:
        raw_audit = f.read()
    print(f"[1/8] Loaded example audit: {len(raw_audit):,} chars")

    # ── Create property data ─────────────────────────────────
    property_data = PropertyData(
        owner_name="Ion Popescu",
        owner_email=TEST_EMAIL,
        property_name="Pensiunea Belvedere",
        property_address="Brașov",
        website_url="https://belvedere-brasov.ro",
        booking_platform_links=["https://booking.com/hotel/ro/pensiunea-belvedere"],
        social_media_links=["https://facebook.com/PensiuneaBelvedere"],
        google_my_business_link="https://maps.google.com/maps/place/Pensiunea+Belvedere+Brasov",
        business_description="Pensiune turistică 3 margarete cu vedere panoramică la munte, 12 camere.",
    )

    # ── Step 1: Insert property into Supabase ────────────────
    db = SupabaseService()
    r = db._table("properties").insert({
        "owner_name": property_data.owner_name,
        "owner_email": property_data.owner_email,
        "property_name": property_data.property_name,
        "property_address": property_data.property_address,
        "website_url": property_data.website_url,
        "booking_platform_links": property_data.booking_platform_links,
        "social_media_links": property_data.social_media_links,
        "google_my_business_link": property_data.google_my_business_link,
        "business_description": property_data.business_description,
        "status": 10,
    }).execute()
    property_id = r.data[0]["id"]
    property_data.id = property_id
    print(f"[2/8] Property inserted: {property_id[:8]}... (status=10 pending)")

    # ── Step 2: Mark as running ──────────────────────────────
    db.update_property_status(property_id, 1)
    db.insert_audit_log(property_id, "E2E test started.", status_text="running")
    print(f"[3/8] Status → 1 (running)")

    # ── Step 3: Insert raw audit result ──────────────────────
    audit_result_id = db.insert_audit_result(property_id, raw_audit)
    db.insert_audit_log(property_id, f"Raw audit stored — {len(raw_audit)} chars", status_text="gemini_success")
    print(f"[4/8] Audit result stored: {audit_result_id[:8]}...")

    # ── Step 4: Template processing (REAL Gemini API call) ───
    print(f"[5/8] Template processing via Gemini (this takes ~10-20 sec)...")
    tp = TemplateProcessor()
    formatted_audit = tp.process_audit_content(
        raw_audit=raw_audit,
        property_data=property_data,
    )
    db.update_audit_result_formatted_data(audit_result_id, formatted_audit)
    db.insert_audit_log(property_id, "Audit formatted.", status_text="formatted")
    print(f"       Formatted: {len(formatted_audit):,} chars")

    # ── Step 5: Generate HTML email ──────────────────────────
    html_content = tp.generate_html_email(
        formatted_content=formatted_audit,
        property_data=property_data,
    )
    print(f"[6/8] HTML email: {len(html_content):,} chars")

    # Save HTML for preview
    with open("/tmp/e2e-test-email.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    # ── Step 6: Generate PDF ─────────────────────────────────
    pdf_bytes = generate_audit_pdf(
        raw_audit=raw_audit,
        property_data=property_data,
        meeting_link=MEETING_LINK,
    )
    db.insert_audit_log(property_id, f"PDF generated — {len(pdf_bytes)/1024:.0f} KB", status_text="pdf_generated")
    print(f"[7/8] PDF: {len(pdf_bytes):,} bytes ({len(pdf_bytes)/1024:.1f} KB)")

    # Save PDF for preview
    with open("/tmp/e2e-test-report.pdf", "wb") as f:
        f.write(pdf_bytes)

    # ── Step 7: Send REAL email via Resend ───────────────────
    print(f"[8/8] Sending REAL email to {TEST_EMAIL}...")
    email_svc = EmailService()
    bcc_list = db.get_report_subscribers()
    print(f"       BCC list: {bcc_list}")

    success = email_svc.send_audit_report(
        property_data=property_data,
        html_content=html_content,
        pdf_bytes=pdf_bytes,
        bcc=bcc_list,
    )

    if success:
        db.insert_audit_log(property_id, "Email sent.", status_text="email_sent")
        db.update_property_status(property_id, 99)
        print(f"       Email SENT successfully!")
    else:
        db.insert_audit_log(property_id, "Email failed.", status_text="email_failed")
        db.update_property_status(property_id, 0)
        print(f"       Email FAILED!")

    # ── Verify logs ──────────────────────────────────────────
    print()
    print("=" * 60)
    print("AUDIT LOGS (from Supabase):")
    print("=" * 60)
    logs = db._table("audit_logs").select("message, status_text, inserted_at").eq("property_id", property_id).order("inserted_at").execute()
    for log in logs.data:
        print(f"  [{log['status_text']}] {log['message']}")

    # ── Final status ─────────────────────────────────────────
    prop = db._table("properties").select("status, status_text").eq("id", property_id).execute()
    final_status = prop.data[0]["status"]
    print()
    print(f"Final property status: {final_status} ({prop.data[0]['status_text']})")
    print()
    print("Files saved:")
    print(f"  Email:  /tmp/e2e-test-email.html")
    print(f"  PDF:    /tmp/e2e-test-report.pdf")
    print()

    if success:
        print("TEST PASSED — Check inbox!")
    else:
        print("TEST FAILED — Check logs above")


if __name__ == "__main__":
    main()
