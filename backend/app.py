"""Flask application factory."""

import logging
import os
import signal
import sys

import sentry_sdk
from flask import Flask
from flask_cors import CORS
from sentry_sdk.integrations.flask import FlaskIntegration

from config import SENTRY_DSN, ALLOWED_ORIGINS

logger = logging.getLogger(__name__)

# ─── Required env vars (validated at startup) ──────────────────
_REQUIRED_ENV_VARS = [
    "GOOGLE_API_KEY",
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "RESEND_API_KEY",
    "BACKEND_API_KEY",
]


def _validate_env_vars() -> None:
    """Raise ValueError if any required env var is missing."""
    missing = [v for v in _REQUIRED_ENV_VARS if not os.environ.get(v)]
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}"
        )


def _setup_sigterm_handler() -> None:
    """Register SIGTERM handler that waits for running pipeline threads."""
    def _handle_sigterm(signum, frame):
        from src.pipeline import RUNNING_THREADS

        alive = [t for t in RUNNING_THREADS if t.is_alive()]
        if alive:
            logger.info(
                "SIGTERM received — waiting for %d pipeline thread(s)...",
                len(alive),
            )
            for t in alive:
                t.join(timeout=5400)
        logger.info("Graceful shutdown complete.")
        sys.exit(0)

    signal.signal(signal.SIGTERM, _handle_sigterm)


def create_app() -> Flask:
    """Create and configure the Flask application."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )

    # Validate required env vars
    _validate_env_vars()

    # Initialize Sentry
    if SENTRY_DSN:
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[FlaskIntegration()],
            traces_sample_rate=0.1,
            environment=os.getenv("FLASK_ENV", "production"),
        )

    app = Flask(__name__)

    # CORS — safety net (browser doesn't call Flask directly, but good practice)
    origins = [o.strip() for o in ALLOWED_ORIGINS.split(",") if o.strip()]
    if os.getenv("FLASK_ENV") == "development":
        origins.append("http://localhost:3000")
    CORS(
        app,
        origins=origins or ["*"],
        allow_headers=["Content-Type", "X-API-Key"],
        methods=["GET", "POST", "OPTIONS"],
    )

    # Register blueprints
    from src.routes import api

    app.register_blueprint(api)

    # Graceful shutdown handler
    _setup_sigterm_handler()

    return app


# Module-level app instance for gunicorn (`gunicorn app:app`)
app = create_app()
