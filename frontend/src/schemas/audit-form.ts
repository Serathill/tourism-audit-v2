import { z } from "zod";
import { ALL_COUNTIES, MAX_DESCRIPTION_LENGTH } from "@/lib/constants";

// ═══════════════════════════════════════════════════════════
// Audit Form — Zod Schemas (shared client + server)
// ═══════════════════════════════════════════════════════════

// ── Helper: normalize URL ──────────────────────────────

function normalizeUrl(val: string): string {
  const trimmed = val.trim();
  if (!trimmed) return trimmed;
  if (!/^https?:\/\//i.test(trimmed)) {
    return `https://${trimmed}`;
  }
  return trimmed;
}

// ── Step 1: Required Fields ────────────────────────────

export const stepOneSchema = z.object({
  owner_name: z
    .string()
    .min(2, "Numele trebuie să aibă cel puțin 2 caractere")
    .max(100, "Numele nu poate depăși 100 de caractere"),
  owner_email: z
    .string()
    .email("Adresa de email nu este validă")
    .max(254, "Adresa de email este prea lungă"),
  property_name: z
    .string()
    .min(2, "Numele proprietății trebuie să aibă cel puțin 2 caractere")
    .max(200, "Numele proprietății nu poate depăși 200 de caractere"),
  property_address: z
    .string()
    .refine((val) => ALL_COUNTIES.includes(val), {
      message: "Selectează un județ valid",
    }),
});

// ── Step 2: Optional Fields ────────────────────────────

export const stepTwoSchema = z.object({
  website_url: z
    .string()
    .default("")
    .transform(normalizeUrl)
    .pipe(z.string().url("URL-ul nu este valid").or(z.literal(""))),
  booking_platform_links: z
    .string()
    .max(2000, "Link-urile nu pot depăși 2000 de caractere")
    .default(""),
  social_media_links: z
    .string()
    .max(2000, "Link-urile nu pot depăși 2000 de caractere")
    .default(""),
  google_my_business_link: z
    .string()
    .default("")
    .transform(normalizeUrl)
    .pipe(z.string().url("URL-ul nu este valid").or(z.literal(""))),
  business_description: z
    .string()
    .max(
      MAX_DESCRIPTION_LENGTH,
      `Descrierea nu poate depăși ${MAX_DESCRIPTION_LENGTH} de caractere`
    )
    .default(""),
});

// ── Combined Schema (full form) ────────────────────────

export const auditFormSchema = stepOneSchema.merge(stepTwoSchema);

// ── Types ──────────────────────────────────────────────

export type StepOneData = z.infer<typeof stepOneSchema>;
export type StepTwoData = z.infer<typeof stepTwoSchema>;
export type AuditFormData = z.infer<typeof auditFormSchema>;

/** Input type for react-hook-form (before Zod transforms/defaults) */
export type AuditFormInput = z.input<typeof auditFormSchema>;
