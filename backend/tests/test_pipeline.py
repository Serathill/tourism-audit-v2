"""Tests for pipeline.py — concurrency, thread cleanup, semaphore."""

import threading
from unittest.mock import patch, MagicMock

from src.pipeline import (
    RUNNING_THREADS,
    MAX_CONCURRENT_AUDITS,
    _cleanup_finished_threads,
    _audit_semaphore,
)
from src.models import PropertyData


def _make_property(**kwargs):
    defaults = {
        "id": "test-id-1234",
        "owner_name": "Test Owner",
        "owner_email": "test@test.com",
        "property_name": "Test Property",
        "property_address": "Brasov",
    }
    defaults.update(kwargs)
    return PropertyData(**defaults)


class TestCleanupFinishedThreads:
    def test_removes_dead_threads(self):
        RUNNING_THREADS.clear()

        dead = threading.Thread(target=lambda: None)
        dead.start()
        dead.join()  # wait for it to finish

        alive = threading.Thread(target=lambda: threading.Event().wait(10), daemon=True)
        alive.start()

        RUNNING_THREADS.extend([dead, alive])
        _cleanup_finished_threads()

        assert len(RUNNING_THREADS) == 1
        assert RUNNING_THREADS[0] is alive

        # Cleanup
        RUNNING_THREADS.clear()

    def test_empty_list_stays_empty(self):
        RUNNING_THREADS.clear()
        _cleanup_finished_threads()
        assert len(RUNNING_THREADS) == 0


class TestConcurrencyLimit:
    def test_semaphore_value(self):
        assert MAX_CONCURRENT_AUDITS == 3

    def test_semaphore_limits_concurrent(self):
        """Verify semaphore blocks after MAX_CONCURRENT_AUDITS acquisitions."""
        # Acquire all permits
        for _ in range(MAX_CONCURRENT_AUDITS):
            assert _audit_semaphore.acquire(blocking=False) is True

        # Next one should fail (non-blocking)
        assert _audit_semaphore.acquire(blocking=False) is False

        # Release all
        for _ in range(MAX_CONCURRENT_AUDITS):
            _audit_semaphore.release()
