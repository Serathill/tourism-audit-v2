"""Tests for Pydantic PropertyData model validators."""

import pytest
from src.models import PropertyData


class TestPropertyData:
    def test_minimal_valid(self):
        p = PropertyData(
            owner_name="Ion Popescu",
            owner_email="ion@test.com",
            property_name="Pensiunea Test",
            property_address="Brasov",
        )
        assert p.owner_name == "Ion Popescu"
        assert p.website_url is None
        assert p.booking_platform_links == []

    def test_empty_string_to_none(self):
        p = PropertyData(
            owner_name="Ion",
            owner_email="ion@test.com",
            property_name="Test",
            property_address="Brasov",
            website_url="",
            google_my_business_link="",
        )
        assert p.website_url is None
        assert p.google_my_business_link is None

    def test_valid_url_kept(self):
        p = PropertyData(
            owner_name="Ion",
            owner_email="ion@test.com",
            property_name="Test",
            property_address="Brasov",
            website_url="https://pensiunea-test.ro",
        )
        assert p.website_url == "https://pensiunea-test.ro"

    def test_empty_list_fallback(self):
        p = PropertyData(
            owner_name="Ion",
            owner_email="ion@test.com",
            property_name="Test",
            property_address="Brasov",
            booking_platform_links=None,
            social_media_links="",
        )
        assert p.booking_platform_links == []
        assert p.social_media_links == []

    def test_list_filters_empty_strings(self):
        p = PropertyData(
            owner_name="Ion",
            owner_email="ion@test.com",
            property_name="Test",
            property_address="Brasov",
            booking_platform_links=["https://booking.com/test", "", "  "],
        )
        assert len(p.booking_platform_links) == 1
        assert p.booking_platform_links[0] == "https://booking.com/test"

    def test_full_property(self):
        p = PropertyData(
            id="abc-123",
            owner_name="Maria Ionescu",
            owner_email="maria@pensiune.ro",
            property_name="Pensiunea Floarea",
            property_address="Sibiu",
            website_url="https://pensiunea-floarea.ro",
            booking_platform_links=["https://booking.com/floarea"],
            social_media_links=["https://facebook.com/floarea"],
            google_my_business_link="https://maps.google.com/floarea",
            business_description="Pensiune cu 8 camere in centrul Sibiului.",
            status=10,
        )
        assert p.id == "abc-123"
        assert p.status == 10
        assert len(p.booking_platform_links) == 1
