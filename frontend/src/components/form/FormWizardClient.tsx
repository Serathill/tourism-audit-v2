"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { ArrowLeft, ArrowRight, Loader2, CheckCircle2, Calendar } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { StepIndicator } from "@/components/form/StepIndicator";
import { StepOneBasic } from "@/components/form/StepOneBasic";
import { StepTwoDetails } from "@/components/form/StepTwoDetails";
import { StepThreeReview } from "@/components/form/StepThreeReview";
import {
  auditFormSchema,
  type AuditFormData,
  type AuditFormInput,
} from "@/schemas/audit-form";
import { HONEYPOT_FIELD_NAME } from "@/lib/constants";
import { getStoredUTMParams } from "@/lib/utm";

type FormWizardClientProps = {
  meetingLink?: string;
};

export function FormWizardClient({ meetingLink }: FormWizardClientProps) {
  const [step, setStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [honeypot, setHoneypot] = useState("");

  const form = useForm<AuditFormInput, unknown, AuditFormData>({
    resolver: zodResolver(auditFormSchema),
    defaultValues: {
      owner_name: "",
      owner_email: "",
      property_name: "",
      property_address: "",
      website_url: "",
      booking_platform_links: "",
      social_media_links: "",
      google_my_business_link: "",
      business_description: "",
    },
    mode: "onBlur",
  });

  async function goToStep(target: number) {
    if (target > step) {
      // Validate current step before advancing
      if (step === 1) {
        const valid = await form.trigger([
          "owner_name",
          "owner_email",
          "property_name",
          "property_address",
        ]);
        if (!valid) return;
      }
      if (step === 2) {
        // Step 2 is optional — just validate what's filled
        const valid = await form.trigger([
          "website_url",
          "booking_platform_links",
          "social_media_links",
          "google_my_business_link",
          "business_description",
        ]);
        if (!valid) return;
      }
    }
    setStep(target);
  }

  async function onSubmit(data: AuditFormData) {
    setIsSubmitting(true);

    try {
      const utmParams = getStoredUTMParams();
      const response = await fetch("/api/audit/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...data,
          ...utmParams,
          [HONEYPOT_FIELD_NAME]: honeypot,
        }),
      });

      const result = await response.json();

      if (!response.ok) {
        if (response.status === 429) {
          toast.error("Prea multe încercări. Te rugăm așteaptă un minut și încearcă din nou.");
        } else if (response.status === 400 && result.errors) {
          // Show first validation error
          const firstError = result.errors[0];
          toast.error(firstError?.message || result.message);
        } else {
          toast.error(result.message || "A apărut o eroare. Te rugăm încearcă din nou.");
        }
        return;
      }

      // Success
      setIsSuccess(true);
    } catch {
      toast.error("Conexiunea a eșuat. Te rugăm încearcă din nou.");
    } finally {
      setIsSubmitting(false);
    }
  }

  // Success state
  if (isSuccess) {
    const propertyName = form.getValues("property_name");
    return (
      <div className="flex flex-col items-center gap-5 py-4 text-center" role="status" aria-live="polite">
        <div className="flex size-14 items-center justify-center rounded-full bg-[var(--success)]/10">
          <CheckCircle2 className="size-7 text-[var(--success)]" />
        </div>
        <div>
          <h3 className="font-display text-xl font-bold text-foreground">
            Cererea a fost trimisă cu succes!
          </h3>
          <p className="mt-2 text-sm text-muted-foreground">
            Analizăm prezența online a <strong>{propertyName}</strong>.
            <br />
            Raportul personalizat ajunge pe email în 30-90 de minute.
          </p>
        </div>

        <div className="w-full rounded-lg border border-border bg-muted/30 p-4 text-left text-sm">
          <p className="mb-2 font-medium text-foreground">Ce urmează:</p>
          <ol className="flex flex-col gap-1.5 text-muted-foreground">
            <li>1. Verifică email-ul (inclusiv folderul Spam)</li>
            <li>2. Primești raportul cu recomandări personalizate</li>
            <li>3. Opțional: programează o consultanță strategică gratuită</li>
          </ol>
        </div>

        {meetingLink && (
          <Button asChild size="lg" className="w-full bg-gradient-cta text-foreground font-semibold shadow-md">
            <a href={meetingLink} target="_blank" rel="noopener noreferrer">
              <Calendar className="size-4" />
              Programează consultanță gratuită
            </a>
          </Button>
        )}
      </div>
    );
  }

  return (
    <form
      onSubmit={form.handleSubmit(onSubmit)}
      noValidate
      aria-label="Formular audit digital"
    >
      {/* Honeypot — hidden from users, traps bots */}
      <div className="absolute -left-[9999px] opacity-0" aria-hidden="true">
        <label htmlFor={HONEYPOT_FIELD_NAME}>Nu completa acest câmp</label>
        <input
          type="text"
          id={HONEYPOT_FIELD_NAME}
          name={HONEYPOT_FIELD_NAME}
          tabIndex={-1}
          autoComplete="off"
          value={honeypot}
          onChange={(e) => setHoneypot(e.target.value)}
        />
      </div>

      {/* Step indicator */}
      <div className="mb-6">
        <StepIndicator currentStep={step} />
      </div>

      {/* Step content */}
      <div className="min-h-[280px]">
        {step === 1 && <StepOneBasic form={form} />}
        {step === 2 && <StepTwoDetails form={form} />}
        {step === 3 && (
          <StepThreeReview form={form} onEditStep={setStep} />
        )}
      </div>

      {/* Navigation buttons */}
      <div className="mt-6 flex gap-3">
        {step > 1 && (
          <Button
            type="button"
            variant="outline"
            onClick={() => setStep(step - 1)}
            disabled={isSubmitting}
            className="flex-1 sm:flex-none"
          >
            <ArrowLeft className="size-4" />
            Înapoi
          </Button>
        )}

        {step < 3 && (
          <Button
            type="button"
            onClick={() => goToStep(step + 1)}
            className="flex-1 bg-gradient-cta text-foreground font-semibold shadow-md hover:shadow-lg transition-shadow"
          >
            Înainte
            <ArrowRight className="size-4" />
          </Button>
        )}

        {step === 3 && (
          <Button
            type="submit"
            disabled={isSubmitting}
            className="flex-1 bg-gradient-cta text-foreground font-semibold shadow-md hover:shadow-lg transition-shadow"
            aria-busy={isSubmitting}
          >
            {isSubmitting ? (
              <>
                <Loader2 className="size-4 animate-spin" />
                Se trimite...
              </>
            ) : (
              "Trimite cererea de audit"
            )}
          </Button>
        )}
      </div>

      {/* Completion time hint */}
      {step === 1 && (
        <p className="mt-3 text-center text-xs text-muted-foreground">
          Completează în 2 minute
        </p>
      )}
    </form>
  );
}
