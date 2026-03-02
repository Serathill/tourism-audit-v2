import logging
import datetime
from typing import Optional

from supabase import create_client, Client

from config import SUPABASE_URL, SUPABASE_KEY, DB_SCHEMA
from src.models import PropertyData

logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    pass


class SupabaseService:
    """Supabase CRUD operations for tourism_audit_v2 schema."""

    def __init__(self) -> None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set.")

        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client initialized.")

    def _table(self, name: str):
        """Access a table in the tourism_audit_v2 schema."""
        return self.client.schema(DB_SCHEMA).table(name)

    # ── Property operations ─────────────────────────────────

    def get_property_by_id(self, property_id: str) -> Optional[PropertyData]:
        try:
            response = (
                self._table("properties")
                .select("*")
                .eq("id", property_id)
                .execute()
            )

            if not response.data:
                logger.warning("Property %s not found.", property_id)
                return None

            return self._to_property_data(response.data[0])
        except Exception as e:
            logger.error("Failed to fetch property %s: %s", property_id, e)
            raise DatabaseError(f"Failed to fetch property {property_id}: {e}")

    def update_property_status(self, property_id: str, status: int) -> bool:
        status_text_map = {10: "pending", 1: "running", 99: "success", 0: "failed"}
        try:
            response = (
                self._table("properties")
                .update(
                    {
                        "status": status,
                        "status_text": status_text_map.get(status, "unknown"),
                        "last_status_update_at": datetime.datetime.now(
                            datetime.timezone.utc
                        ).isoformat(),
                    }
                )
                .eq("id", property_id)
                .execute()
            )
            if response.data:
                logger.info("Property %s status → %d", property_id, status)
                return True
            return False
        except Exception as e:
            logger.error("Failed to update status for %s: %s", property_id, e)
            raise DatabaseError(f"Failed to update status for {property_id}: {e}")

    # ── Audit result operations ─────────────────────────────

    def insert_audit_result(
        self, property_id: str, raw_data: str
    ) -> Optional[str]:
        try:
            response = (
                self._table("audit_results")
                .insert({"property_id": property_id, "raw_data": raw_data})
                .execute()
            )
            if response.data:
                audit_result_id = response.data[0].get("id")
                logger.info(
                    "Inserted audit result for %s: %s", property_id, audit_result_id
                )
                return audit_result_id
            return None
        except Exception as e:
            logger.error("Failed to insert audit result for %s: %s", property_id, e)
            raise DatabaseError(
                f"Failed to insert audit result for {property_id}: {e}"
            )

    def update_audit_result_formatted_data(
        self, audit_result_id: str, formatted_data: str
    ) -> bool:
        try:
            response = (
                self._table("audit_results")
                .update({"formatted_data": formatted_data})
                .eq("id", audit_result_id)
                .execute()
            )
            if response.data:
                logger.info("Updated formatted data for audit result %s", audit_result_id)
                return True
            return False
        except Exception as e:
            logger.error(
                "Failed to update formatted data for %s: %s", audit_result_id, e
            )
            raise DatabaseError(
                f"Failed to update formatted data for {audit_result_id}: {e}"
            )

    # ── Audit log operations ────────────────────────────────

    def insert_audit_log(
        self,
        property_id: str,
        message: str,
        status_text: Optional[str] = None,
    ) -> bool:
        try:
            data: dict = {"property_id": property_id, "message": message}
            if status_text is not None:
                data["status_text"] = status_text

            response = self._table("audit_logs").insert(data).execute()
            if response.data:
                logger.info("Audit log [%s]: %s", property_id[:8], message)
                return True
            return False
        except Exception as e:
            logger.error("Failed to insert audit log for %s: %s", property_id, e)
            raise DatabaseError(f"Failed to insert audit log for {property_id}: {e}")

    # ── Report subscribers ──────────────────────────────────

    def get_report_subscribers(self) -> list[str]:
        try:
            response = (
                self._table("report_subscribers")
                .select("email")
                .eq("rate_limit_exempt", True)
                .execute()
            )
            if not response.data:
                return []
            return [row["email"] for row in response.data]
        except Exception as e:
            logger.error("Failed to fetch report subscribers: %s", e)
            return []

    # ── Helpers ─────────────────────────────────────────────

    def _to_property_data(self, row: dict) -> PropertyData:
        try:
            booking_links = row.get("booking_platform_links") or []
            social_links = row.get("social_media_links") or []

            # Handle JSONB that might come as strings
            if isinstance(booking_links, str):
                import json
                booking_links = json.loads(booking_links)
            if isinstance(social_links, str):
                import json
                social_links = json.loads(social_links)

            return PropertyData(
                id=row.get("id"),
                owner_name=row.get("owner_name", ""),
                owner_email=row.get("owner_email", ""),
                property_name=row.get("property_name", ""),
                property_address=row.get("property_address", ""),
                website_url=row.get("website_url"),
                booking_platform_links=booking_links,
                social_media_links=social_links,
                google_my_business_link=row.get("google_my_business_link"),
                business_description=row.get("business_description"),
                status=row.get("status"),
                last_status_update_at=row.get("last_status_update_at"),
            )
        except Exception as e:
            logger.error("Failed to convert DB row to PropertyData: %s", e)
            raise DatabaseError(f"Failed to convert DB row: {e}")
