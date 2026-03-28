import { AlertCircle } from "lucide-react";

const PAIN_POINTS = [
  "Vizibilitate redusă online",
  "Dificultăți în a atrage o audiență clară și relevantă",
  "Lipsa unei echipe interne de marketing sau cunoștințe în domeniu",
  "Dorința de a înțelege clar ce poți îmbunătăți rapid fără efort suplimentar",
  "Majoritatea rezervărilor vin prin platforme externe cu comisioane mari",
] as const;

export function AudienceSection() {
  return (
    <section
      aria-labelledby="audience-heading"
      className="bg-[var(--bg-secondary)]"
    >
      <div className="mx-auto max-w-[1200px] px-4 py-16 sm:px-6 md:py-20">
        <h2
          id="audience-heading"
          className="mb-6 text-center font-display text-[clamp(1.5rem,3vw,2rem)] font-bold tracking-tight text-foreground"
        >
          Pentru cine este acest audit?
        </h2>

        <p className="mx-auto mb-10 max-w-2xl text-center text-lg leading-relaxed text-muted-foreground">
          Acest audit gratuit este creat special pentru proprietarii și managerii
          de unități de cazare deosebite din România: pensiuni boutique, tiny
          houses, A-frames și alte case de vacanță cu potențial de creștere.
        </p>

        <div className="mx-auto max-w-2xl">
          <p className="mb-4 font-medium text-foreground">
            Te regăsești în una din aceste situații?
          </p>
          <ul className="space-y-3">
            {PAIN_POINTS.map((point) => (
              <li key={point} className="flex items-start gap-3">
                <AlertCircle className="mt-0.5 size-5 shrink-0 text-amber-500" />
                <span className="text-muted-foreground">{point}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
