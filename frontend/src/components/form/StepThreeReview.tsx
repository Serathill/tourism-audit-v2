"use client";

import type { UseFormReturn } from "react-hook-form";
import type { AuditFormInput } from "@/schemas/audit-form";
import { Pencil } from "lucide-react";

type StepThreeReviewProps = {
  form: UseFormReturn<AuditFormInput>;
  onEditStep: (step: number) => void;
};

function ReviewRow({ label, value }: { label: string; value: string }) {
  if (!value) return null;
  return (
    <div className="flex flex-col gap-0.5">
      <dt className="text-xs font-medium text-muted-foreground">{label}</dt>
      <dd className="break-words text-sm text-foreground">{value}</dd>
    </div>
  );
}

export function StepThreeReview({ form, onEditStep }: StepThreeReviewProps) {
  const data = form.getValues();

  const hasOptionalData =
    data.website_url ||
    data.booking_platform_links ||
    data.social_media_links ||
    data.google_my_business_link ||
    data.business_description;

  return (
    <div className="flex flex-col gap-6">
      <p className="text-sm text-muted-foreground">
        Verifică datele înainte de a trimite cererea de audit.
      </p>

      {/* Required data */}
      <div className="rounded-lg border border-border bg-muted/30 p-4">
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-sm font-semibold text-foreground">Datele tale</h3>
          <button
            type="button"
            onClick={() => onEditStep(1)}
            className="inline-flex items-center gap-1 text-xs font-medium text-primary transition-colors hover:text-brand-teal-dark"
          >
            <Pencil className="size-3" />
            Editează
          </button>
        </div>
        <dl className="flex flex-col gap-3">
          <ReviewRow label="Nume complet" value={data.owner_name} />
          <ReviewRow label="Email" value={data.owner_email} />
          <ReviewRow label="Numele pensiunii" value={data.property_name} />
          <ReviewRow label="Județul" value={data.property_address} />
        </dl>
      </div>

      {/* Optional data */}
      <div className="rounded-lg border border-border bg-muted/30 p-4">
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-sm font-semibold text-foreground">
            Detalii suplimentare
            {!hasOptionalData && (
              <span className="ml-1.5 text-xs font-normal text-muted-foreground">
                (nu ai completat)
              </span>
            )}
          </h3>
          <button
            type="button"
            onClick={() => onEditStep(2)}
            className="inline-flex items-center gap-1 text-xs font-medium text-primary transition-colors hover:text-brand-teal-dark"
          >
            <Pencil className="size-3" />
            Editează
          </button>
        </div>
        {hasOptionalData ? (
          <dl className="flex flex-col gap-3">
            <ReviewRow label="Website" value={data.website_url || ""} />
            <ReviewRow
              label="Platforme booking"
              value={data.booking_platform_links || ""}
            />
            <ReviewRow
              label="Social media"
              value={data.social_media_links || ""}
            />
            <ReviewRow
              label="Google My Business"
              value={data.google_my_business_link || ""}
            />
            <ReviewRow
              label="Descriere"
              value={data.business_description || ""}
            />
          </dl>
        ) : (
          <p className="text-xs text-muted-foreground">
            Nu ai completat detalii suplimentare - auditul va fi generat pe baza
            informațiilor publice disponibile.
          </p>
        )}
      </div>
    </div>
  );
}
