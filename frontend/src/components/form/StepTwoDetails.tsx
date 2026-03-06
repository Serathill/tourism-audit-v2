"use client";

import type { UseFormReturn } from "react-hook-form";
import type { AuditFormInput } from "@/schemas/audit-form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { MAX_DESCRIPTION_LENGTH } from "@/lib/constants";

type StepTwoDetailsProps = {
  form: UseFormReturn<AuditFormInput>;
};

export function StepTwoDetails({ form }: StepTwoDetailsProps) {
  const {
    register,
    watch,
    formState: { errors },
  } = form;

  const descriptionLength = (watch("business_description") || "").length;

  return (
    <div className="flex flex-col gap-4">
      <p className="text-sm text-muted-foreground">
        Aceste informații sunt opționale, dar ne ajută să generăm un raport mai
        detaliat.
      </p>

      {/* Website URL */}
      <div>
        <Label htmlFor="website_url">
          Website URL <span className="text-muted-foreground">(opțional)</span>
        </Label>
        <Input
          id="website_url"
          type="url"
          placeholder="ex: pensiuneaflorilor.ro"
          autoComplete="url"
          aria-invalid={!!errors.website_url}
          aria-describedby={errors.website_url ? "website_url-error" : undefined}
          className="mt-1.5 h-11"
          {...register("website_url")}
        />
        {errors.website_url && (
          <p id="website_url-error" className="mt-1 text-sm text-destructive" role="alert">
            {errors.website_url.message}
          </p>
        )}
      </div>

      {/* Booking platform links */}
      <div>
        <Label htmlFor="booking_platform_links">
          Link-uri platforme booking{" "}
          <span className="text-muted-foreground">(opțional)</span>
        </Label>
        <Textarea
          id="booking_platform_links"
          placeholder={"ex: booking.com/pensiunea-florilor\nairbnb.com/rooms/123456"}
          rows={3}
          aria-invalid={!!errors.booking_platform_links}
          aria-describedby={errors.booking_platform_links ? "booking_platform_links-error" : undefined}
          className="mt-1.5"
          {...register("booking_platform_links")}
        />
        <p className="mt-1 text-xs text-muted-foreground">
          Câte un link pe fiecare rând
        </p>
        {errors.booking_platform_links && (
          <p id="booking_platform_links-error" className="mt-1 text-sm text-destructive" role="alert">
            {errors.booking_platform_links.message}
          </p>
        )}
      </div>

      {/* Social media links */}
      <div>
        <Label htmlFor="social_media_links">
          Link-uri social media{" "}
          <span className="text-muted-foreground">(opțional)</span>
        </Label>
        <Textarea
          id="social_media_links"
          placeholder={"ex: facebook.com/pensiuneaflorilor\ninstagram.com/pensiuneaflorilor"}
          rows={3}
          aria-invalid={!!errors.social_media_links}
          aria-describedby={errors.social_media_links ? "social_media_links-error" : undefined}
          className="mt-1.5"
          {...register("social_media_links")}
        />
        <p className="mt-1 text-xs text-muted-foreground">
          Câte un link pe fiecare rând
        </p>
        {errors.social_media_links && (
          <p id="social_media_links-error" className="mt-1 text-sm text-destructive" role="alert">
            {errors.social_media_links.message}
          </p>
        )}
      </div>

      {/* Google My Business */}
      <div>
        <Label htmlFor="google_my_business_link">
          Link Google My Business{" "}
          <span className="text-muted-foreground">(opțional)</span>
        </Label>
        <Input
          id="google_my_business_link"
          type="url"
          placeholder="ex: g.co/kgs/xyz sau maps.google.com/..."
          aria-invalid={!!errors.google_my_business_link}
          aria-describedby={errors.google_my_business_link ? "google_my_business_link-error" : undefined}
          className="mt-1.5 h-11"
          {...register("google_my_business_link")}
        />
        {errors.google_my_business_link && (
          <p id="google_my_business_link-error" className="mt-1 text-sm text-destructive" role="alert">
            {errors.google_my_business_link.message}
          </p>
        )}
      </div>

      {/* Business description */}
      <div>
        <Label htmlFor="business_description">
          Descriere business{" "}
          <span className="text-muted-foreground">(opțional)</span>
        </Label>
        <Textarea
          id="business_description"
          placeholder="Descrie pe scurt unitatea ta de cazare, serviciile oferite și ce te diferențiază..."
          rows={4}
          aria-invalid={!!errors.business_description}
          aria-describedby={errors.business_description ? "business_description-error" : undefined}
          className="mt-1.5"
          {...register("business_description")}
        />
        <p className={`mt-1 text-xs ${descriptionLength > MAX_DESCRIPTION_LENGTH - 50 ? "text-destructive" : "text-muted-foreground"}`}>
          {descriptionLength} / {MAX_DESCRIPTION_LENGTH} caractere
        </p>
        {errors.business_description && (
          <p id="business_description-error" className="mt-1 text-sm text-destructive" role="alert">
            {errors.business_description.message}
          </p>
        )}
      </div>
    </div>
  );
}
