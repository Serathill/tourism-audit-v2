from pydantic import BaseModel, Field, field_validator
from typing import Optional
import datetime


class PropertyData(BaseModel):
    """V2 simplified property data model.
    Maps to tourism_audit_v2.properties table.
    """

    id: Optional[str] = None
    owner_name: str
    owner_email: str
    property_name: str
    property_address: str  # county (judet)
    website_url: Optional[str] = None
    booking_platform_links: list[str] = Field(default_factory=list)
    social_media_links: list[str] = Field(default_factory=list)
    google_my_business_link: Optional[str] = None
    business_description: Optional[str] = None
    status: Optional[int] = None
    last_status_update_at: Optional[datetime.datetime] = None

    @field_validator("website_url", "google_my_business_link", mode="before")
    @classmethod
    def empty_str_to_none(cls, v: object) -> object:
        if v == "" or v is None:
            return None
        return v

    @field_validator("booking_platform_links", "social_media_links", mode="before")
    @classmethod
    def empty_list_fallback(cls, v: object) -> object:
        if v in ("", None):
            return []
        if isinstance(v, list):
            return [item for item in v if isinstance(item, str) and item.strip()]
        return v
