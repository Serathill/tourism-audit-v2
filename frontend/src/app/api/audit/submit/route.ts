import { NextResponse } from "next/server";
import { headers } from "next/headers";
import * as Sentry from "@sentry/nextjs";
import { auditFormSchema } from "@/schemas/audit-form";
import { checkRateLimit, getClientIp, RATE_LIMITS } from "@/lib/rate-limit";
import { isHoneypotFilled } from "@/lib/honeypot";
import { verifyRecaptcha } from "@/lib/recaptcha";
import { createServiceClient } from "@/lib/supabase/service";

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

export async function POST(request: Request) {
  try {
    // ── 1. Rate limit check ──────────────────────────────
    const headersList = await headers();
    const ip = getClientIp(headersList);

    const { success: rateLimitOk } = await checkRateLimit(
      ip,
      RATE_LIMITS.auditSubmit
    );
    if (!rateLimitOk) {
      return NextResponse.json(
        { message: "Prea multe cereri. Încercați din nou în câteva minute." },
        { status: 429 }
      );
    }

    // ── 2. Parse body ────────────────────────────────────
    const body = await request.json();

    // ── 3. Honeypot check ────────────────────────────────
    // Silent fake success — bot doesn't know it was rejected
    if (isHoneypotFilled(body)) {
      return NextResponse.json(
        {
          message: "Audit solicitat cu succes.",
          data: { property_id: crypto.randomUUID() },
        },
        { status: 200 }
      );
    }

    // ── 4. reCAPTCHA verification (skip if not configured) ──
    const recaptchaToken = body.recaptcha_token;
    if (recaptchaToken) {
      const { success: captchaOk } = await verifyRecaptcha(recaptchaToken);
      if (!captchaOk) {
        return NextResponse.json(
          {
            message:
              "Verificarea de securitate a eșuat. Te rugăm încearcă din nou.",
          },
          { status: 403 }
        );
      }
    }

    // ── 5. Zod schema validation ─────────────────────────
    const parsed = auditFormSchema.safeParse(body);
    if (!parsed.success) {
      return NextResponse.json(
        {
          message: "Date invalide.",
          errors: parsed.error.issues.map((issue) => ({
            path: issue.path,
            message: issue.message,
          })),
        },
        { status: 400 }
      );
    }

    const data = parsed.data;

    // ── 6. Business logic ────────────────────────────────

    const supabase = createServiceClient();

    // Check if email domain is blocked
    const emailDomain = data.owner_email.split("@")[1]?.toLowerCase();
    if (emailDomain) {
      const { data: blocked } = await supabase
        .from("blocked_emails")
        .select("email")
        .eq("email", emailDomain)
        .maybeSingle();

      if (blocked) {
        // Silent fake success for blocked emails
        return NextResponse.json(
          {
            message: "Audit solicitat cu succes.",
            data: { property_id: crypto.randomUUID() },
          },
          { status: 200 }
        );
      }
    }

    // ── 7. Insert into Supabase ──────────────────────────
    // Parse textarea fields into JSONB arrays
    const bookingLinks = data.booking_platform_links
      ? data.booking_platform_links
          .split("\n")
          .map((s) => s.trim())
          .filter(Boolean)
      : [];

    const socialLinks = data.social_media_links
      ? data.social_media_links
          .split("\n")
          .map((s) => s.trim())
          .filter(Boolean)
      : [];

    const { data: property, error: insertError } = await supabase
      .from("properties")
      .insert({
        owner_name: escapeHtml(data.owner_name),
        owner_email: data.owner_email,
        property_name: escapeHtml(data.property_name),
        property_address: escapeHtml(data.property_address),
        website_url: data.website_url || null,
        booking_platform_links: bookingLinks.length > 0 ? bookingLinks : null,
        social_media_links: socialLinks.length > 0 ? socialLinks : null,
        google_my_business_link: data.google_my_business_link || null,
        business_description: data.business_description
          ? escapeHtml(data.business_description)
          : null,
        status: 10, // pending
      })
      .select("id")
      .single();

    if (insertError) {
      console.error("Supabase insert error:", insertError);
      return NextResponse.json(
        { message: "Eroare internă. Vă rugăm încercați din nou." },
        { status: 500 }
      );
    }

    // ── 8. Trigger backend audit pipeline ────────────────
    // TODO [post-MVP]: Activate reCAPTCHA v3 server-side validation.
    //   Currently only honeypot + rate limit protect against bots.
    //   A sophisticated bot could spam Gemini API requests (costly).
    //   See step 4 above and Known Limitations #8 in PRODUCTION-DEPLOY-PLAN.md.
    const backendUrl = process.env.BACKEND_API_URL;
    const backendApiKey = process.env.BACKEND_API_KEY;

    if (backendUrl && backendApiKey && property?.id) {
      // Fire-and-forget with 10s timeout — don't block user response
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10_000);

      fetch(`${backendUrl}/api/generate-audit`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": backendApiKey,
        },
        body: JSON.stringify({ property_id: property.id }),
        signal: controller.signal,
      })
        .catch((err) => {
          if (err.name === "AbortError") {
            console.warn(
              "Backend trigger timed out (10s) — audit may still start if Render responds later"
            );
          } else {
            console.error("Backend trigger failed:", err);
          }
        })
        .finally(() => clearTimeout(timeoutId));
    }

    // ── 9. Success response ──────────────────────────────
    return NextResponse.json(
      {
        message: "Audit solicitat cu succes.",
        data: { property_id: property?.id },
      },
      { status: 200 }
    );
  } catch (error) {
    console.error("Audit submit error:", error);
    Sentry.captureException(error);
    return NextResponse.json(
      { message: "Eroare internă. Vă rugăm încercați din nou." },
      { status: 500 }
    );
  }
}
