"use client";

import type { UseFormReturn } from "react-hook-form";
import type { AuditFormInput } from "@/schemas/audit-form";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { CountyAutocomplete } from "@/components/form/CountyAutocomplete";

type StepOneBasicProps = {
  form: UseFormReturn<AuditFormInput>;
};

export function StepOneBasic({ form }: StepOneBasicProps) {
  const {
    register,
    setValue,
    watch,
    formState: { errors },
  } = form;

  const countyValue = watch("property_address");

  return (
    <div className="flex flex-col gap-4">
      {/* Nume complet */}
      <div>
        <Label htmlFor="owner_name">
          Nume complet <span className="text-destructive" aria-hidden="true">*</span>
        </Label>
        <Input
          id="owner_name"
          placeholder="ex: Maria Popescu"
          autoComplete="name"
          aria-required="true"
          aria-invalid={!!errors.owner_name}
          aria-describedby={errors.owner_name ? "owner_name-error" : undefined}
          className="mt-1.5 h-11"
          {...register("owner_name")}
        />
        {errors.owner_name && (
          <p id="owner_name-error" className="mt-1 text-sm text-destructive" role="alert">
            {errors.owner_name.message}
          </p>
        )}
      </div>

      {/* Email */}
      <div>
        <Label htmlFor="owner_email">
          Email <span className="text-destructive" aria-hidden="true">*</span>
        </Label>
        <Input
          id="owner_email"
          type="email"
          placeholder="ex: maria@email.com"
          autoComplete="email"
          aria-required="true"
          aria-invalid={!!errors.owner_email}
          aria-describedby={errors.owner_email ? "owner_email-error" : undefined}
          className="mt-1.5 h-11"
          {...register("owner_email")}
        />
        {errors.owner_email && (
          <p id="owner_email-error" className="mt-1 text-sm text-destructive" role="alert">
            {errors.owner_email.message}
          </p>
        )}
      </div>

      {/* Numele pensiunii */}
      <div>
        <Label htmlFor="property_name">
          Numele pensiunii <span className="text-destructive" aria-hidden="true">*</span>
        </Label>
        <Input
          id="property_name"
          placeholder="ex: Pensiunea Florilor"
          autoComplete="organization"
          aria-required="true"
          aria-invalid={!!errors.property_name}
          aria-describedby={errors.property_name ? "property_name-error" : undefined}
          className="mt-1.5 h-11"
          {...register("property_name")}
        />
        {errors.property_name && (
          <p id="property_name-error" className="mt-1 text-sm text-destructive" role="alert">
            {errors.property_name.message}
          </p>
        )}
      </div>

      {/* Județul */}
      <div>
        <Label>
          Județul <span className="text-destructive" aria-hidden="true">*</span>
        </Label>
        <div className="mt-1.5">
          <CountyAutocomplete
            value={countyValue}
            onChange={(val) => setValue("property_address", val, { shouldValidate: true })}
            error={errors.property_address?.message}
          />
        </div>
        {errors.property_address && (
          <p id="property_address-error" className="mt-1 text-sm text-destructive" role="alert">
            {errors.property_address.message}
          </p>
        )}
      </div>
    </div>
  );
}
