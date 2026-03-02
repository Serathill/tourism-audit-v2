import { Check } from "lucide-react";
import { cn } from "@/lib/utils";
import { MAX_FORM_STEPS } from "@/lib/constants";

const STEP_LABELS = ["Datele tale", "Detalii", "Verificare"] as const;

type StepIndicatorProps = {
  currentStep: number;
};

export function StepIndicator({ currentStep }: StepIndicatorProps) {
  return (
    <div className="flex items-center gap-2" role="navigation" aria-label={`Pas ${currentStep} din ${MAX_FORM_STEPS}`}>
      {Array.from({ length: MAX_FORM_STEPS }, (_, i) => {
        const step = i + 1;
        const isActive = step === currentStep;
        const isCompleted = step < currentStep;

        return (
          <div key={step} className="flex items-center gap-2">
            {/* Step circle */}
            <div
              className={cn(
                "flex size-7 items-center justify-center rounded-full text-xs font-bold transition-colors",
                isCompleted && "bg-[var(--success)] text-white",
                isActive && "bg-primary text-white",
                !isActive && !isCompleted && "border border-border text-muted-foreground"
              )}
              aria-current={isActive ? "step" : undefined}
            >
              {isCompleted ? <Check className="size-3.5" /> : step}
            </div>

            {/* Step label (hidden on very small screens) */}
            <span
              className={cn(
                "hidden text-xs sm:inline",
                isActive ? "font-medium text-foreground" : "text-muted-foreground"
              )}
            >
              {STEP_LABELS[i]}
            </span>

            {/* Connector line */}
            {step < MAX_FORM_STEPS && (
              <div
                className={cn(
                  "h-0.5 w-6 rounded-full sm:w-10",
                  step < currentStep ? "bg-[var(--success)]" : "bg-border"
                )}
              />
            )}
          </div>
        );
      })}

      {/* Step count on mobile */}
      <span className="ml-auto text-xs text-muted-foreground sm:hidden">
        Pas {currentStep} din {MAX_FORM_STEPS}
      </span>
    </div>
  );
}
