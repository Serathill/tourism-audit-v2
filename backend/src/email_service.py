"""Email delivery via Resend with retry + exponential backoff."""

import html
import logging
import time

import resend

from config import RESEND_API_KEY, FROM_EMAIL
from src.models import PropertyData

logger = logging.getLogger(__name__)


class EmailError(Exception):
    pass


class EmailService:
    """Send audit emails via Resend."""

    def __init__(self) -> None:
        if not RESEND_API_KEY:
            raise ValueError("RESEND_API_KEY must be set.")
        resend.api_key = RESEND_API_KEY
        logger.info("Resend client initialized.")

    def send_audit_report(
        self,
        property_data: PropertyData,
        html_content: str,
        pdf_bytes: bytes | None = None,
        bcc: list[str] | None = None,
        retry_count: int = 3,
        retry_delay: int = 2,
    ) -> bool:
        """Send the audit report email with retry + exponential backoff.

        If pdf_bytes is provided, attaches it as a PDF file to the email.
        """
        subject = (
            f"Raportul tau digital - {property_data.property_name}"
        )

        email_data: dict = {
            "from": FROM_EMAIL,
            "to": property_data.owner_email,
            "subject": subject,
            "html": html_content,
            "text": (
                f"Salut, {property_data.owner_name},\n\n"
                "Te rugăm să vizualizezi acest email într-un client "
                "de email care suportă HTML pentru a vedea raportul complet."
            ),
        }

        if pdf_bytes:
            # Resend SDK accepts List[int] from bytes
            pdf_filename = (
                f"Audit-Digital-{property_data.property_name.replace(' ', '-')}.pdf"
            )
            email_data["attachments"] = [
                {
                    "filename": pdf_filename,
                    "content": list(pdf_bytes),
                }
            ]
            logger.info(
                "Attaching PDF: %s (%.1f KB)",
                pdf_filename,
                len(pdf_bytes) / 1024,
            )

        if bcc:
            email_data["bcc"] = bcc

        delay = retry_delay
        for attempt in range(1, retry_count + 1):
            try:
                logger.info(
                    "Sending audit email to %s (attempt %d/%d)",
                    property_data.owner_email,
                    attempt,
                    retry_count,
                )
                response = resend.Emails.send(email_data)

                if response and "id" in response:
                    logger.info("Email sent — ID: %s", response["id"])
                    return True

                logger.warning("Unexpected Resend response: %s", response)
            except Exception as e:
                logger.error(
                    "Email send error (attempt %d/%d): %s",
                    attempt,
                    retry_count,
                    e,
                )
                if attempt < retry_count:
                    logger.info("Retrying in %ds...", delay)
                    time.sleep(delay)
                    delay *= 2

        logger.error(
            "Failed to send email after %d attempts.", retry_count
        )
        return False

    def send_email_raw(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str,
        cc: list[str] | None = None,
    ) -> bool:
        """Send a raw email with arbitrary subject/body."""
        email_data = {
            "from": FROM_EMAIL,
            "to": to_email,
            "subject": subject,
            "html": html_content,
            "text": text_content,
        }
        if cc:
            email_data["cc"] = cc

        try:
            response = resend.Emails.send(email_data)
            if response and "id" in response:
                logger.info("Raw email sent to %s — ID: %s", to_email, response["id"])
                return True
            logger.warning("Unexpected Resend response: %s", response)
            return False
        except Exception as e:
            logger.error("Error sending raw email to %s: %s", to_email, e)
            return False

    def send_internal_failure_alert(
        self,
        primary_to: str,
        cc_emails: list[str],
        property_name: str | None,
        owner_email: str,
        error_context: str,
    ) -> bool:
        """Send a technical failure alert to the team."""
        safe_property = html.escape(property_name or "Unknown")
        safe_email = html.escape(owner_email)
        safe_context = html.escape(error_context)
        subject = f"[ALERT] Audit failure - {safe_property}"
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color:#111;">
            <h3 style="margin:0 0 10px 0;">Audit failure alert</h3>
            <ul>
                <li><strong>Property</strong>: {safe_property}</li>
                <li><strong>Owner email</strong>: {safe_email}</li>
                <li><strong>Context</strong>: {safe_context}</li>
            </ul>
            <p>Verificati <code>audit_logs</code> si <code>audit_results</code>.
            Clientul a fost notificat automat.</p>
        </body>
        </html>
        """
        text_content = (
            f"Audit failure alert\n"
            f"Property: {property_name or 'N/A'}\n"
            f"Owner email: {owner_email}\n"
            f"Context: {error_context}\n"
            "Clientul a fost notificat. Verificati audit_logs/audit_results."
        )
        try:
            payload: dict = {
                "from": FROM_EMAIL,
                "to": primary_to,
                "subject": subject,
                "html": html_content,
                "text": text_content,
            }
            if cc_emails:
                payload["cc"] = cc_emails
            response = resend.Emails.send(payload)
            return bool(response and "id" in response)
        except Exception as e:
            logger.error("Error sending internal alert to %s: %s", primary_to, e)
            return False

    def send_error_notification(
        self,
        to_email: str,
        property_name: str | None,
        error_message: str,
    ) -> bool:
        """Notify the customer about an error (no technical details)."""
        subject = "Notificare privind auditul digital - intervenim imediat"
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color:#111;">
            <p>Salut,</p>
            <p>{error_message}</p>
            <p>Cu drag,<br/>Echipa DeviDevs</p>
        </body>
        </html>
        """
        text_content = f"Salut,\n\n{error_message}\n\nCu drag,\nEchipa DeviDevs"

        try:
            response = resend.Emails.send(
                {
                    "from": FROM_EMAIL,
                    "to": to_email,
                    "subject": subject,
                    "html": html_content,
                    "text": text_content,
                }
            )
            return bool(response and "id" in response)
        except Exception as e:
            logger.error("Error sending error notification to %s: %s", to_email, e)
            return False
