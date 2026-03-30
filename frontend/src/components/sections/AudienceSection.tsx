import { CheckCircle } from "lucide-react";

const PAIN_POINTS = [
  "Ai investit in renovari si amenajari, dar camerele stau goale in extrasezon",
  "Rezervarile vin aproape doar prin Booking, iar comisioanele cresc de la an la an",
  "Ai o pagina de Facebook, poate si un site, dar nu stii daca te gaseste cineva pe Google",
  "Concurenta din zona pare ca are mereu plin, desi tu oferi conditii la fel de bune",
  "Ai incercat sa faci 'ceva marketing', dar nu ai vazut rezultate concrete",
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
          Daca iti recunosti situatia aici, auditul e facut pentru tine
        </h2>

        <p className="mx-auto mb-10 max-w-2xl text-center text-lg leading-relaxed text-muted-foreground">
          Pensiuni, tiny houses, A-frames, glampinguri, case de vacanta, hoteluri mici:
        </p>

        <div className="mx-auto max-w-2xl">
          <ul className="space-y-3">
            {PAIN_POINTS.map((point) => (
              <li key={point} className="flex items-start gap-3">
                <CheckCircle className="mt-0.5 size-5 shrink-0 text-primary" />
                <span className="text-muted-foreground">{point}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
