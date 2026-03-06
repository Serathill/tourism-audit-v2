"""3-phase audit pipeline orchestrator.
Runs in a background thread: Deep Research → Template → Email.
"""

import logging
import threading

from src.audit_generator import GeminiAuditor, AuditGenerationError
from src.template_processor import TemplateProcessor, TemplateProcessingError
from src.pdf_generator import generate_audit_pdf
from src.email_service import EmailService, EmailError
from src.database_service import SupabaseService, DatabaseError
from src.models import PropertyData
from config import MEETING_LINK

logger = logging.getLogger(__name__)


def run_audit_pipeline(property_data: PropertyData) -> None:
    """Execute the full 3-phase audit pipeline.

    Phase 1: Gemini Deep Research (30-90 min)
    Phase 2: Template formatting via Gemini
    Phase 3: HTML email generation + delivery via Resend

    This function is designed to run in a daemon thread.
    """
    property_id = property_data.id
    audit_result_id = None

    # Initialize services
    try:
        db_service = SupabaseService()
    except Exception as e:
        logger.error("Failed to init SupabaseService: %s", e)
        return

    email_service = None
    try:
        email_service = EmailService()
    except Exception as e:
        logger.warning("Failed to init EmailService: %s", e)

    def _notify_client_error(message: str) -> None:
        """Send a user-friendly error notification (once)."""
        if getattr(_notify_client_error, "_sent", False):
            return
        try:
            svc = email_service
            if svc is None:
                try:
                    svc = EmailService()
                except Exception:
                    return
            ok = svc.send_error_notification(
                to_email=property_data.owner_email,
                property_name=property_data.property_name,
                error_message=message,
            )
            if ok:
                db_service.insert_audit_log(
                    property_id,
                    "Client notified about error.",
                    status_text="client_notified_error",
                )
            _notify_client_error._sent = True
        except Exception as e:
            logger.error("Failed to notify client: %s", e)

    def _notify_team_failure(error_context: str) -> None:
        """Send internal failure alert to team subscribers."""
        try:
            subscribers = db_service.get_report_subscribers()
            if not subscribers:
                return
            svc = email_service
            if svc is None:
                try:
                    svc = EmailService()
                except Exception:
                    return
            svc.send_internal_failure_alert(
                primary_to=subscribers[0],
                cc_emails=subscribers[1:],
                property_name=property_data.property_name,
                owner_email=property_data.owner_email,
                error_context=error_context,
            )
        except Exception as e:
            logger.error("Failed to send internal failure alert: %s", e)

    # Mark as running
    try:
        db_service.update_property_status(property_id, 1)
        db_service.insert_audit_log(
            property_id, "Audit pipeline started.", status_text="running"
        )
    except DatabaseError as e:
        logger.error("Failed to update initial status: %s", e)

    try:
        # ── Phase 1: Gemini Deep Research ────────────────────
        logger.info(
            "PHASE 1: Deep Research — %s", property_data.property_name
        )

        auditor = GeminiAuditor()
        raw_audit = auditor.start_audit_generation(property_data)

        audit_result_id = db_service.insert_audit_result(
            property_id, raw_audit
        )
        db_service.insert_audit_log(
            property_id,
            f"Deep Research complete — {len(raw_audit)} chars",
            status_text="gemini_success",
        )

        # ── Phase 2: Template Processing ─────────────────────
        logger.info("PHASE 2: Template Processing")

        template_processor = TemplateProcessor()
        formatted_audit = template_processor.process_audit_content(
            raw_audit=raw_audit, property_data=property_data
        )

        if audit_result_id:
            db_service.update_audit_result_formatted_data(
                audit_result_id, formatted_audit
            )
        db_service.insert_audit_log(
            property_id, "Audit formatted.", status_text="formatted"
        )

        # ── Phase 3: PDF + Email Delivery ─────────────────────
        logger.info(
            "PHASE 3: PDF + Email Delivery → %s", property_data.owner_email
        )

        html_content = template_processor.generate_html_email(
            formatted_content=formatted_audit, property_data=property_data
        )

        # Generate full PDF report from raw audit
        pdf_bytes = None
        try:
            pdf_bytes = generate_audit_pdf(
                raw_audit=raw_audit,
                property_data=property_data,
                meeting_link=MEETING_LINK,
            )
            db_service.insert_audit_log(
                property_id,
                f"PDF generated — {len(pdf_bytes) / 1024:.0f} KB",
                status_text="pdf_generated",
            )
        except Exception as e:
            logger.error("PDF generation failed (non-fatal): %s", e)
            db_service.insert_audit_log(
                property_id,
                f"PDF generation failed: {e}",
                status_text="pdf_error",
            )
            # Continue without PDF — email summary is still sent

        # Get BCC list for internal team
        bcc_list = db_service.get_report_subscribers()

        if email_service is None:
            email_service_local = EmailService()
        else:
            email_service_local = email_service

        success = email_service_local.send_audit_report(
            property_data=property_data,
            html_content=html_content,
            pdf_bytes=pdf_bytes,
            bcc=bcc_list,
        )

        if success:
            logger.info("Audit pipeline completed successfully.")
            db_service.insert_audit_log(
                property_id, "Email sent.", status_text="email_sent"
            )
            db_service.update_property_status(property_id, 99)
        else:
            logger.error("Email delivery failed.")
            db_service.insert_audit_log(
                property_id,
                "Email delivery failed.",
                status_text="email_failed",
            )
            db_service.update_property_status(property_id, 0)
            _notify_team_failure("Email delivery failed after retries")

    except AuditGenerationError as e:
        error_str = str(e)
        logger.error("Audit generation error: %s", e)
        db_service.insert_audit_log(
            property_id, f"Gemini error: {e}", status_text="gemini_error"
        )
        db_service.update_property_status(property_id, 0)
        _notify_team_failure(f"AuditGenerationError: {e}")

        if "QUOTA_ERROR" in error_str:
            _notify_client_error(
                "Din cauza volumului mare de solicitari, auditul nu a putut fi "
                "generat momentan. Te rugam sa incerci din nou mai tarziu."
            )
        else:
            _notify_client_error(
                "Din cauza unei probleme tehnice temporare, auditul nu a putut "
                "fi generat. Te rugam sa incerci din nou mai tarziu."
            )

    except TemplateProcessingError as e:
        logger.error("Template processing error: %s", e)
        db_service.insert_audit_log(
            property_id,
            f"Template error: {e}",
            status_text="template_error",
        )
        db_service.update_property_status(property_id, 0)
        _notify_team_failure(f"TemplateProcessingError: {e}")
        _notify_client_error(
            "A aparut o problema la procesarea auditului. Echipa noastra "
            "a fost notificata si lucram la rezolvare."
        )

    except Exception as e:
        logger.error("Unexpected pipeline error: %s", e)
        db_service.insert_audit_log(
            property_id,
            f"Unexpected error: {e}",
            status_text="unexpected_error",
        )
        db_service.update_property_status(property_id, 0)
        _notify_team_failure(f"Unexpected: {e}")
        _notify_client_error(
            "A aparut o eroare neasteptata. Echipa noastra a fost notificata "
            "si lucram la rezolvare."
        )


# Module-level list of running pipeline threads (for graceful shutdown)
RUNNING_THREADS: list[threading.Thread] = []


def start_pipeline_thread(property_data: PropertyData) -> threading.Thread:
    """Launch the audit pipeline in a non-daemon thread."""
    thread = threading.Thread(
        target=run_audit_pipeline,
        args=(property_data,),
        daemon=False,
        name=f"audit-{property_data.id[:8]}",
    )
    RUNNING_THREADS.append(thread)
    thread.start()
    logger.info(
        "Pipeline thread started for '%s' (id: %s)",
        property_data.property_name,
        property_data.id,
    )
    return thread
