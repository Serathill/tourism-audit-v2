import os
from dotenv import load_dotenv

load_dotenv()

# ─── Google Gemini AI ──────────────────────────────────────
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_DEEP_RESEARCH_MODEL = os.getenv(
    "GEMINI_DEEP_RESEARCH_MODEL", "deep-research-pro-preview-12-2025"
)
GEMINI_FORMATTER_MODEL = os.getenv(
    "GEMINI_FORMATTER_MODEL", "gemini-3-pro-preview"
)

# ─── Supabase ─────────────────────────────────────────────
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
DB_SCHEMA = "tourism_audit_v2"

# ─── Email (Resend) ──────────────────────────────────────
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "Audit Digital Turism <no-reply@audit-turism.ro>")

# ─── API Auth ────────────────────────────────────────────
BACKEND_API_KEY = os.getenv("BACKEND_API_KEY", "")

# ─── Meeting Link ───────────────────────────────────────
MEETING_LINK = os.getenv("MEETING_LINK", "")

# ─── CORS ────────────────────────────────────────────────
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "")

# ─── Error Tracking ─────────────────────────────────────
SENTRY_DSN = os.getenv("SENTRY_DSN", "")

# ─── Pipeline Tuning ────────────────────────────────────
AUDIT_POLL_INTERVAL = int(os.getenv("AUDIT_POLL_INTERVAL", "30"))
AUDIT_MAX_WAIT_MINUTES = int(os.getenv("AUDIT_MAX_WAIT_MINUTES", "90"))
