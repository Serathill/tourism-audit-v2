"""Gemini Deep Research audit generator.
Uses the Interactions API (async polling) for autonomous web research.
Quality-first: no cost constraints, 50-100+ searches per audit.
"""

import logging
import time
from datetime import datetime

from google import genai

from config import (
    GOOGLE_API_KEY,
    GEMINI_DEEP_RESEARCH_MODEL,
    AUDIT_POLL_INTERVAL,
    AUDIT_MAX_WAIT_MINUTES,
)
from src.models import PropertyData
from src.quality_filter import QualityFilter

logger = logging.getLogger(__name__)


class AuditGenerationError(Exception):
    pass


class GeminiAuditor:
    """Gemini Deep Research auditor — quality-first approach."""

    def __init__(self) -> None:
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY must be set.")

        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        logger.info(
            "Gemini Deep Research initialized — model: %s",
            GEMINI_DEEP_RESEARCH_MODEL,
        )

    def _build_master_prompt(self, property_data: PropertyData) -> str:
        current_date = datetime.now().strftime("%Y-%m-%d")

        booking_links = (
            ", ".join(property_data.booking_platform_links)
            if property_data.booking_platform_links
            else "Not provided"
        )
        social_links = (
            ", ".join(property_data.social_media_links)
            if property_data.social_media_links
            else "Not provided"
        )

        return f"""
# Tourism Digital Audit — Deep Research Directive

**CRITICAL CONTEXT:**
Today's date is {current_date}. Use this date for web search context, recent reviews, current GMB data, and latest social media posts. When searching, prioritize recent data (2025-2026) over outdated information.

## Quality Mandate

**Cost is NOT a constraint.** Perform 60-120+ web searches per audit. Quality trumps speed. A mediocre audit that arrives in 30 minutes is worse than a comprehensive one that takes 90 minutes.

**The bar:** The output must be good enough that the property owner forwards it to their accountant, partner, or local tourism association saying "uite ce au găsit despre noi."

## Role

You are a top-tier digital marketing auditor specializing in Romanian accommodation businesses. Your mission is to conduct a detailed, actionable audit using ONLY publicly available information. The final report is written for the property owner.

## Tone & Language Rules

### Address Form
- Use **"tu"** (informal Romanian) — NOT "dumneavoastră"
- "Afacerea ta", "site-ul tău", "profilul tău", "oaspeții tăi"
- Voice: Confident, direct, warm — like a knowledgeable friend who is a marketing expert
- Solution-oriented — frame gaps as opportunities, not failures
- Specific and data-backed — numbers, percentages, comparisons

### FORBIDDEN Language (Quality Filter catches these post-generation)
NEVER use these phrases in the Romanian output — they destroy credibility:
"nu am putut", "nu s-a putut", "nu a fost posibil", "nu am reușit",
"nu am avut acces", "nu am putut extrage", "nu am putut obține",
"nu am putut verifica", "nu am putut confirma", "nu am putut măsura",
"limitări de acces", "restricții de acces", "nu a fost disponibil"

INSTEAD, transform limitations into recommendations:
- BAD: "Nu am putut obține scorul PageSpeed"
- GOOD: "Pentru optimizarea performanței, recomandăm rularea unui test PageSpeed Insights și implementarea recomandărilor pentru a atinge ținta de 70+/100 pe mobil"

## Input Data — Property to Audit

- **Property Name:** {property_data.property_name}
- **County (Județ):** {property_data.property_address}
- **Description:** {property_data.business_description or "Not provided."}
- **Website:** {property_data.website_url or "Not provided"}
- **Booking Platforms:** {booking_links}
- **Social Media:** {social_links}
- **Google My Business:** {property_data.google_my_business_link or "Not provided"}

**CRITICAL:** Treat ALL provided links defensively. If any link is a placeholder ("cauta tu", "poti cauta?"), broken, or lacks a valid domain, IGNORE it and proactively search for the correct official page.

---

## Research Execution Strategy

**Use parallel search agents for speed and depth.** Run 8 tracks simultaneously:

```
Agent Track 1: Website analysis (PageSpeed, SSL, mobile, SEO, Schema.org)
Agent Track 2: Google Maps / Google Business Profile
Agent Track 3: Booking.com, TripAdvisor, Airbnb listings
Agent Track 4: Facebook, Instagram, TikTok presence
Agent Track 5: Review aggregation across all platforms
Agent Track 6: Competitor discovery and benchmarking
Agent Track 7: Community & forum sentiment (Romanian forums, Facebook groups, Reddit, travel blogs)
Agent Track 8: Business registry & tourism compliance (ONRC, listafirme.ro, clasificare turism)
```

**Minimum 60 unique web searches per audit. Target 80-120.**

---

## Research Phases

### Phase 1: Property Discovery & Identification

**Objective:** Find ALL digital touchpoints for this property, even if the owner didn't provide them.

**Actions:**
1. Search: `"{property_data.property_name}" {property_data.property_address}` — find official website, listings, mentions
2. Search: `"{property_data.property_name}" booking.com` — find Booking.com listing
3. Search: `"{property_data.property_name}" tripadvisor` — find TripAdvisor listing
4. Search: `"{property_data.property_name}" airbnb` — find Airbnb listing
5. Search: `"{property_data.property_name}" facebook` — find Facebook page
6. Search: `"{property_data.property_name}" instagram` — find Instagram profile
7. Search: `site:google.com/maps "{property_data.property_name}"` — find Google Business Profile
8. If website_url provided, fetch it and extract all outbound links to social/booking profiles
9. Cross-reference: Do all profiles point to the same property? Flag discrepancies.

**Data to Extract:**
- Official website URL (verified working or not found)
- All booking platform listings (with direct URLs)
- All social media profiles (with direct URLs)
- Google Business Profile URL
- Any other digital presence (blog, YouTube, local directories)
- Discrepancies between profiles (different phone numbers, addresses, names)

### Phase 2: Website Technical Performance

**Objective:** Evaluate the website as a booking conversion tool, not just its existence.

**Actions:**
1. Fetch the website homepage
2. Search: `site:pagespeed.web.dev` or access PageSpeed Insights for the URL
3. Check SSL certificate (HTTPS vs HTTP, valid/expired)
4. Test mobile viewport meta tag presence
5. Analyze CTA visibility — is there a clear "Rezervă" / "Book Now" button above the fold?
6. Check URL structure (clean URLs vs query strings)
7. Fetch 3-5 internal pages (rooms, contact, about, gallery)
8. Check for booking engine integration (direct booking vs redirect to OTA)

**Data to Extract:**
- PageSpeed score (mobile + desktop, numeric)
- SSL status (valid HTTPS / expired / HTTP only)
- Mobile-friendliness (viewport, touch targets, font sizes)
- CTA analysis (exists, visible, above fold, compelling text)
- Navigation clarity (can a visitor find rooms + prices in 2 clicks?)
- Booking engine (direct booking capability or OTA-only?)
- Page load observations (heavy images, blocking scripts, etc.)

**Scoring Rubric:**
| Score | Criteria |
|-------|----------|
| 9-10 | Fast (PageSpeed 90+), HTTPS, mobile-perfect, clear CTA, direct booking |
| 7-8 | Decent speed (70-89), HTTPS, mobile-friendly, CTA exists |
| 5-6 | Slow (50-69), HTTPS, mobile issues, CTA hard to find |
| 3-4 | Very slow (<50), or HTTP, or not mobile-friendly |
| 1-2 | Broken site, no HTTPS, no mobile, no CTA |
| 0 | No website exists |

### Phase 3: SEO Foundation

**Objective:** Evaluate how well the website is optimized for search engines.

**Actions:**
1. View page source — extract `<title>` and `<meta name="description">` for homepage and 2-3 key pages
2. Analyze H1/H2 heading structure
3. Sample 10-15 images — check alt text (descriptive, empty, missing)
4. Search for Schema.org markup (JSON-LD: LodgingBusiness, Hotel, LocalBusiness)
5. Check for sitemap.xml and robots.txt
6. Analyze internal linking structure
7. Check for canonical URLs
8. Verify hreflang tags (Romanian + English minimum for tourism)

**Scoring Rubric:**
| Score | Criteria |
|-------|----------|
| 9-10 | Title+meta on all pages, Schema.org, sitemap, alt text >80%, multilingual |
| 7-8 | Title+meta on homepage, some alt text, no Schema.org |
| 5-6 | Generic title, missing meta description, poor alt text |
| 3-4 | No SEO optimization at all |
| 0 | No website |

### Phase 4: Search Visibility & Local SEO

**Objective:** How easy is it for potential guests to FIND this property on Google?

**Actions:**
1. Search Google: `cazare {{property_type}} {{location}}` — note position (top 3, top 10, not found)
2. Search Google: `"{property_data.property_name}"` — note what appears
3. Search Google: `pensiune {property_data.property_address}` — note if property appears
4. Search Google Maps: `{property_data.property_name} {property_data.property_address}` — find GMB listing
5. If GMB exists, extract: rating, review count, photos count, address, phone, website link, categories, recent posts, Q&A
6. Check if property appears in Google Hotel Pack / Local Pack
7. Search: `{property_data.property_name} recenzii` — note what review sources appear

**Scoring Rubric:**
| Score | Criteria |
|-------|----------|
| 9-10 | Top 3 for local keywords, complete GMB, 50+ photos, 100+ reviews, regular posts |
| 7-8 | Top 10, GMB exists with good data, 20+ photos, 50+ reviews |
| 5-6 | Page 2, GMB incomplete, few photos, some reviews |
| 3-4 | Barely findable, GMB unclaimed or minimal |
| 1-2 | Not findable on Google for relevant terms |

### Phase 5: Booking Platform Presence

**Objective:** Analyze presence and quality on the platforms where tourists actually book.

**Actions:**
1. Fetch Booking.com listing — extract: rating, review count, room types, photos, description, amenities, price range, badges
2. Fetch TripAdvisor listing — extract: rating, review count, ranking in area, traveler photos, management responses
3. Fetch Airbnb listing (if applicable) — extract: rating, review count, Superhost status, photos, description
4. Check for presence on: Pensiuni.info, TurismMaramures, Travelminit.ro, or regional tourism directories
5. Compare photo quality across platforms (same photos or different?)
6. Check description quality (copy-paste or unique per platform?)

**Data to Extract per Platform:**
- Rating (numeric), Review count, Photos count and quality
- Description completeness and quality, Amenities listed
- Badges/awards (Booking Genius, Superhost, etc.)
- Management response rate to reviews
- Ranking in local area (TripAdvisor)

**Scoring Rubric:**
| Score | Criteria |
|-------|----------|
| 9-10 | 3+ platforms, all with 8.5+ rating, 100+ reviews, 30+ photos, complete descriptions |
| 7-8 | 2+ platforms, ratings 7.5+, good photos, decent descriptions |
| 5-6 | 1-2 platforms, ratings 7.0+, few photos, generic descriptions |
| 3-4 | Only 1 platform, low ratings, poor photos |
| 1-2 | Listed but essentially empty profiles |
| 0 | Not on any booking platform |

### Phase 6: Social Media Presence

**Objective:** Evaluate social media as a guest acquisition and engagement channel.

**Actions:**
1. Fetch Facebook page — extract: followers, recent posts (last 10), engagement (likes/comments/shares), content types
2. Fetch Instagram profile — extract: followers, posts count, recent posts, engagement rate, Reels presence, Stories highlights
3. Check for TikTok presence
4. Check for YouTube channel
5. Analyze content types (photos, videos, Reels, Stories, UGC)
6. Calculate engagement rate: (avg likes + comments) / followers x 100
7. Note posting frequency (posts per week/month)
8. Check for UGC (User Generated Content) — sharing guest posts?

**Scoring Rubric:**
| Score | Criteria |
|-------|----------|
| 9-10 | 2+ active platforms, 3+ posts/week, >3% engagement, Reels/Stories, UGC |
| 7-8 | 2 platforms, 1-2 posts/week, decent engagement |
| 5-6 | 1 platform somewhat active, low engagement |
| 3-4 | Account exists but rarely posts (last post >1 month ago) |
| 1-2 | Account exists but abandoned (last post >6 months) |
| 0 | No social media presence |

### Phase 7: Online Reputation & Reviews

**Objective:** Aggregate and analyze reputation across ALL review sources.

**Actions:**
1. Collect reviews from: Google (GMB), Booking.com, TripAdvisor, Airbnb, Facebook
2. Calculate aggregate rating (weighted by review count)
3. Identify top 3 positive themes with example quotes
4. Identify top 3 negative themes with example quotes
5. Analyze owner response rate per platform
6. Analyze owner response quality (generic vs personalized)
7. Check for review trends (improving or declining over time?)

**Scoring Rubric:**
| Score | Criteria |
|-------|----------|
| 9-10 | 200+ reviews, 9.0+ aggregate, >80% response rate, personalized responses |
| 7-8 | 100+ reviews, 8.5+, responds to most reviews |
| 5-6 | 50+ reviews, 8.0+, inconsistent responses |
| 3-4 | <50 reviews, 7.0-7.9, rarely responds |
| 1-2 | <20 reviews, or <7.0 rating, never responds |
| 0 | No reviews anywhere |

### Phase 8: Content & Photography Quality

**Objective:** Assess the visual and written content quality across all channels.

**Actions:**
1. Evaluate photo quality on website (professional vs phone, resolution, lighting, staging)
2. Compare photos across platforms (same set or different? updated recently?)
3. Check photo count (30+ recommended for booking platforms)
4. Evaluate description quality (SEO-friendly? Compelling? Unique per platform?)
5. Check for blog or content marketing on the website
6. Check multilingual content (Romanian + English minimum for international tourists)

**Scoring Rubric:**
| Score | Criteria |
|-------|----------|
| 9-10 | Professional photos, 50+ across platforms, unique descriptions, blog active, multilingual |
| 7-8 | Good photos, 30+, decent descriptions |
| 5-6 | OK photos, 15-30, generic descriptions |
| 3-4 | Poor photos, <15, minimal descriptions |
| 1-2 | Very few/low quality photos, no descriptions |

### Phase 9: Competitive Landscape

**Objective:** Position this property against its direct competitors with hard data.

**Actions:**
1. Search: `cazare {{location}}` — identify top 5 competitors by Google ranking
2. Search: `pensiune {{location}} booking.com` — find competitors on Booking
3. For each competitor, quickly extract: rating, review count, PageSpeed (if they have a website), social media follower count
4. Compare prices if visible on booking platforms
5. Identify what competitors do better (and worse)
6. Find the property's competitive advantages

### Phase 9B: Community & Forum Sentiment

**Objective:** Get unfiltered, real traveler perception from forums, blogs, and community discussions.

**Actions:**
1. Search: `"{property_data.property_name}" site:reddit.com` — check r/romania, r/travel, r/solotravel
2. Search: `"{property_data.property_name}" forum` — find Romanian travel forums
3. Search: `"{property_data.property_name}" blog recenzie` — find travel blog reviews
4. Search: `cazare {{location}} recomandare site:reddit.com` — area recommendations
5. Search: `cazare {{location}} recomandare forum` — Romanian forum recommendations
6. Search: `"{property_data.property_name}" OR "cazare {{location}}" site:facebook.com` — public Facebook group mentions
7. Search: `"{property_data.property_name}" parere experienta` — personal experience posts
8. Search: `"cazare {property_data.property_address}" blog top pensiuni` — travel blogs ranking

**Key Insight:** Zero forum/blog presence means the property relies 100% on OTA traffic. This is both a risk (OTA dependency) and an opportunity (untapped organic discovery channels).

**Scoring Rubric:**
| Score | Criteria |
|-------|----------|
| 9-10 | Featured in 3+ travel blogs, recommended on forums, appears in "top X" lists |
| 7-8 | Mentioned in 2+ blogs/forums, positive sentiment |
| 5-6 | 1-2 mentions, mixed sentiment |
| 3-4 | Barely any mentions, only automated directory listings |
| 1-2 | Zero organic mentions — invisible outside booking platforms |

### Phase 9C: Business Registry & Tourism Compliance

**Objective:** Verify the business is legally registered, properly classified for tourism, and compliant.

**Actions:**
1. Search: `"{property_data.property_name}" site:listafirme.ro` — find business registration
2. Search: `"{property_data.property_name}" site:termene.ro` — check for legal issues
3. Search: `"{property_data.property_name}" CUI` or `cod fiscal` — find fiscal code
4. Search: `"{property_data.property_name}" clasificare turism` — Ministry of Tourism classification
5. Search: `"{property_data.property_name}" site:turism.gov.ro` — official tourism registry
6. Search: `"{property_data.property_name}" ANTREC` or `FPTR` — tourism association membership
7. Check if Google Business Profile category matches official classification

**Note:** This is NOT about judging the operator. It's about identifying easy wins: "Dacă ai clasificarea oficială dar nu apare pe Google Business Profile, pierzi vizibilitate gratuită."

**Scoring Rubric:**
| Score | Criteria |
|-------|----------|
| 9-10 | Active registration, official tourism classification, association membership, all consistent |
| 7-8 | Active registration, classification exists, minor inconsistencies |
| 5-6 | Registered but no tourism classification found |
| 3-4 | Registration found but issues (wrong CAEN, no classification) |
| 1-2 | Cannot find registration, or concerning legal signals |

### Phase 10: Scoring Summary

**Objective:** Aggregate all phase scores into a single digital health assessment.

Score ALL 11 categories (0-10 each):
1. Prezență Digitală (Phase 1)
2. Website Tehnic (Phase 2)
3. SEO Tehnic (Phase 3)
4. Vizibilitate Google (Phase 4)
5. Platforme Booking (Phase 5)
6. Social Media (Phase 6)
7. Reputație & Recenzii (Phase 7)
8. Conținut & Fotografii (Phase 8)
9. Poziție Competitivă (Phase 9)
10. Comunitate & Forumuri (Phase 9B)
11. Conformitate Turism (Phase 9C)

**Total: X/110 (XX%)**

Verdict levels:
| Level | Score | Interpretation |
|-------|-------|----------------|
| Excelent | 90-110 | Printre cei mai bine poziționați din zonă |
| Bine | 72-89 | Fundament solid, oportunități clare de creștere |
| Mediu | 50-71 | Potențial, dar pierzi vizibilitate și rezervări |
| Sub medie | 28-49 | Necesită acțiune urgentă pe mai multe fronturi |
| Critic | 0-27 | Prezența digitală aproape inexistentă |

### Phase 11: Action Plan & Recommendations

Deliver a prioritized, actionable plan:

**Acțiuni Imediate (Această Săptămână)** — 3 quick wins with impact and estimated time
**Acțiuni pe Termen Scurt (Luna Aceasta)** — 3 medium-term improvements
**Acțiuni Strategice (Următoarele 3 Luni)** — 2 strategic investments
**Ce Poți Face Singur vs. Ce Necesită Ajutor Expert** — split for clarity

Each action MUST be SPECIFIC (not generic "improve SEO") and include estimated IMPACT with industry benchmarks:
- PageSpeed: "1 second improvement = +7% conversions (Google data), 53% abandon sites >3s"
- HTTPS: "94% of Romanian sites have SSL; Google penalizes HTTP with -15% visibility"
- Mobile: "61% of bookings from mobile; mobile-friendly = +40% conversions"
- GMB: "Optimized GMB = +70% direct calls, 5x more Local Pack appearances"
- Reviews: "Properties with 20+ reviews see +65% conversion rate"
- Social: "4+ posts/week = +60% direct bookings"
- Schema.org: "4x more Hotel Pack appearances, +30-40% organic traffic in 3 months"

### Phase 12: Sources & References

List ALL sources consulted, organized by category. Minimum 60 sources. Every inline citation must have a corresponding entry here.

### Phase 13: Consultation Bridge

Naturally transition from audit value to consultation offer. This audit covered only public information. A complete analysis would include: internal analytics, personalized content strategy, revenue management, email marketing, Booking.com dependency reduction.

---

## Cross-Reference Requirements

The audit MUST cross-reference data across sources:
1. **Phone/address consistency** — Does phone on website match GMB, Booking, Facebook?
2. **Photo freshness** — Same old photos everywhere, or updated seasonally?
3. **Description consistency** — All platforms describe same amenities and room types?
4. **Rating alignment** — Large differences may indicate fake reviews or platform-specific issues
5. **Price parity** — Is direct booking price competitive with OTA prices?
6. **Classification vs GMB category** — Does official tourism classification match Google Business category?
7. **Business name consistency** — Registered name matches Booking, Google, website?
8. **Forum sentiment vs official reviews** — Do forums paint a different picture than curated reviews?

Flag any discrepancies found with specific details and fix recommendations.

---

## Quality Standards — Minimum Requirements

- All 13 phases completed (or marked N/A with reason for website phases if no website)
- At least 60 unique web searches performed
- All 11 category scores assigned (0-10 scale)
- Total digital health score calculated (X/110)
- At least 3 competitors benchmarked with comparative data
- At least 3 positive and 3 negative review themes extracted with quotes
- Inline citations `[source.com]` for every data point
- Sources section with all sources organized by category
- Community/forum search performed (even if zero results — document the search)
- Business registry check performed (listafirme.ro, turism.gov.ro)
- All action plan items are SPECIFIC (not generic)
- Zero forbidden language phrases
- "Tu" address form used throughout
- Romanian language throughout (natural, not translated)
- Minimum total output: 6,000+ characters

---

## Final Output Requirements

**The entire report MUST be written in Romanian.**

Structure the output into 3 sections + appendix:

```
Section 1: Prezența Online și Vizibilitate
  → Phase 1 (Discovery) + Phase 2 (Website) + Phase 3 (SEO) + Phase 4 (Google) + Phase 5 (Booking)

Section 2: Conținut, Reputație și Comunitate
  → Phase 6 (Social Media) + Phase 7 (Reviews) + Phase 8 (Content Quality) + Phase 9B (Community & Forums)

Section 3: Oportunități și Plan de Acțiune
  → Phase 9 (Competitive) + Phase 9C (Compliance) + Phase 10 (Scoring) + Phase 11 (Action Plan) + Phase 13 (Consultation)

Appendix: Surse & Referințe
  → Phase 12 (Sources — always included at the end)
```

Use markdown tables for structured data (ratings, scores, comparisons).
Use status icons: ✅ (score 7-10), ⚠️ (score 4-6), ❌ (score 0-3).
Include inline citations `[source.com]` for ALL data points.
"""

    def start_audit_generation(self, property_data: PropertyData) -> str:
        """Generate audit using Gemini Deep Research.
        Returns raw audit text in Romanian.
        """
        logger.info(
            "Starting Deep Research for '%s' (model: %s)",
            property_data.property_name,
            GEMINI_DEEP_RESEARCH_MODEL,
        )

        master_prompt = self._build_master_prompt(property_data)

        try:
            # Create interaction with background=True (Interactions API)
            initial_interaction = self.client.interactions.create(
                input=master_prompt,
                agent=GEMINI_DEEP_RESEARCH_MODEL,
                background=True,
            )

            interaction_id = initial_interaction.id
            logger.info("Research started — interaction: %s", interaction_id)

            # Poll for completion
            max_wait = AUDIT_MAX_WAIT_MINUTES * 60
            elapsed = 0

            while elapsed < max_wait:
                interaction = self.client.interactions.get(interaction_id)
                status = interaction.status
                minutes = elapsed // 60

                logger.info("[%02dm] Status: %s", minutes, status)

                if status == "completed":
                    if not interaction.outputs:
                        raise AuditGenerationError(
                            "Deep Research completed but returned empty outputs"
                        )
                    raw_audit_text = interaction.outputs[-1].text

                    logger.info(
                        "Deep Research complete — %d chars in %d min",
                        len(raw_audit_text),
                        minutes,
                    )

                    # Apply quality filter
                    quality_filter = QualityFilter()
                    audit_text, filter_report = quality_filter.process_audit(
                        raw_audit_text
                    )

                    if filter_report["filtered"]:
                        logger.info(
                            "Quality filter: %d violations removed",
                            filter_report["improvement"],
                        )

                    return audit_text

                elif status in ("failed", "cancelled"):
                    error_msg = f"Deep Research failed: {status}"
                    if hasattr(interaction, "error") and interaction.error:
                        error_msg += f" — {interaction.error}"
                    logger.error(error_msg)
                    raise AuditGenerationError(error_msg)

                time.sleep(AUDIT_POLL_INTERVAL)
                elapsed += AUDIT_POLL_INTERVAL

            # Timeout
            logger.error(
                "Deep Research timeout after %d minutes (interaction: %s)",
                AUDIT_MAX_WAIT_MINUTES,
                interaction_id,
            )
            raise AuditGenerationError(
                f"Timeout after {AUDIT_MAX_WAIT_MINUTES} min (interaction: {interaction_id})"
            )

        except AuditGenerationError:
            raise
        except Exception as e:
            error_str = str(e).lower()

            if any(
                kw in error_str
                for kw in ("quota", "insufficient", "credit", "resource")
            ):
                logger.error("Gemini quota/credit error: %s", e)
                raise AuditGenerationError(f"QUOTA_ERROR: {e}")

            if any(kw in error_str for kw in ("api", "key", "auth")):
                logger.error("Gemini API auth error: %s", e)
                raise AuditGenerationError(f"API_AUTH_ERROR: {e}")

            logger.error("Gemini Deep Research failed: %s", e)
            raise AuditGenerationError(f"GEMINI_ERROR: {e}")
