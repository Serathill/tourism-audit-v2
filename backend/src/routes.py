"""Flask routes — /healthz + /api/generate-audit + /api/daily-report."""

import datetime
import logging
from functools import wraps

from flask import Blueprint, jsonify, request

from config import BACKEND_API_KEY
from src.database_service import SupabaseService, DatabaseError
from src.email_service import EmailService
from src.pipeline import start_pipeline_thread

logger = logging.getLogger(__name__)

api = Blueprint("api", __name__)


def require_api_key(f):
    """Validate X-API-Key header."""

    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-Key", "")
        if not BACKEND_API_KEY or api_key != BACKEND_API_KEY:
            logger.warning("Unauthorized request — invalid API key")
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)

    return decorated


@api.route("/healthz", methods=["GET"])
def health_check():
    """Health check endpoint for Render."""
    logger.debug("Health check pinged")
    return jsonify({"status": "ok"}), 200


@api.route("/api/generate-audit", methods=["POST"])
@require_api_key
def generate_audit():
    """Accept audit request, launch pipeline in background thread.
    Returns 202 Accepted immediately.
    """
    data = request.get_json(silent=True)
    if not data or "property_id" not in data:
        return jsonify({"error": "property_id is required"}), 400

    property_id = data["property_id"]
    logger.info("Audit request received for property: %s", property_id)

    try:
        db_service = SupabaseService()
        property_data = db_service.get_property_by_id(property_id)

        if not property_data:
            return jsonify({"error": "Property not found"}), 404

        # Duplicate submission guard
        if property_data.status in (1, 99):
            msg = (
                "Audit already in progress"
                if property_data.status == 1
                else "Audit already completed"
            )
            return jsonify({"error": msg}), 409

        # Launch pipeline in background thread
        start_pipeline_thread(property_data)

        return (
            jsonify(
                {
                    "status": "accepted",
                    "property_id": property_id,
                    "message": "Audit pipeline started",
                }
            ),
            202,
        )

    except DatabaseError as e:
        logger.error("Database error for property %s: %s", property_id, e)
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        logger.error("Unexpected error for property %s: %s", property_id, e)
        return jsonify({"error": "Internal server error"}), 500


@api.route("/api/daily-report", methods=["POST"])
@require_api_key
def daily_report():
    """Generate and send daily audit summary report.

    Called by Supabase pg_cron every day at 09:00 Bucharest time.
    Reports on yesterday's audit activity.
    """
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    try:
        db_service = SupabaseService()
        metrics = db_service.get_audit_counts_for_day(yesterday)

        subscribers = db_service.get_report_subscribers()
        if not subscribers:
            logger.warning("No report subscribers configured.")
            return jsonify({"status": "skipped", "reason": "no subscribers"}), 200

        primary_to = subscribers[0]
        cc_list = subscribers[1:] if len(subscribers) > 1 else []

        date_str = yesterday.strftime("%d.%m.%Y")
        subject = f"Raport zilnic audituri - {date_str}"

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color:#111;">
            <h2 style="margin:0 0 15px 0;">Raport zilnic - {date_str}</h2>
            <ul style="line-height: 1.8;">
                <li><strong>Audituri pornite:</strong> {metrics['started']}</li>
                <li><strong>Audituri finalizate cu succes:</strong> {metrics['completed']}</li>
                <li><strong>Audituri esuate:</strong> {metrics['failed']}</li>
                <li><strong>Audituri inca in curs (stuck):</strong> {metrics['running']}</li>
            </ul>
            <p style="color:#666; font-size:13px; margin-top:20px;">
                Pentru detalii, verificati <code>tourism_audit_v2.audit_logs</code>
                si <code>tourism_audit_v2.properties</code> in Supabase.
            </p>
            <p style="color:#999; font-size:12px;">Generat automat de Audit Digital Turism</p>
        </body>
        </html>
        """

        text_content = (
            f"Raport zilnic - {date_str}\n\n"
            f"Audituri pornite: {metrics['started']}\n"
            f"Audituri finalizate: {metrics['completed']}\n"
            f"Audituri esuate: {metrics['failed']}\n"
            f"Audituri in curs (stuck): {metrics['running']}\n\n"
            "Verificati audit_logs si properties in Supabase."
        )

        email_service = EmailService()
        sent = email_service.send_email_raw(
            to_email=primary_to,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            cc=cc_list,
        )

        if sent:
            db_service.insert_audit_log(
                None,
                f"Daily report sent to {primary_to} + {len(cc_list)} CC",
                status_text="daily_report_sent",
            )
            logger.info("Daily report sent to %s", primary_to)
            return jsonify({"status": "sent", "to": primary_to, "metrics": metrics}), 200

        logger.error("Failed to send daily report email.")
        return jsonify({"status": "error", "reason": "email send failed"}), 500

    except DatabaseError as e:
        logger.error("Database error in daily report: %s", e)
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        logger.error("Unexpected error in daily report: %s", e)
        return jsonify({"error": "Internal server error"}), 500
