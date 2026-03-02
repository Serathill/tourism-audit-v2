"""Flask routes — /healthz + /api/generate-audit."""

import logging
from functools import wraps

from flask import Blueprint, jsonify, request

from config import BACKEND_API_KEY
from src.database_service import SupabaseService, DatabaseError
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
