import { CheckCircle } from "lucide-react";

const PAIN_POINTS = [
  "Proprietari de pensiuni boutique, tiny houses, A-frames, glampinguri si case de vacanta cu potential de crestere",
  "Hoteluri mici si medii care vor mai multe rezervari directe, nu doar prin Booking sau Airbnb",
  "Proprietari de cazari inedite (cabane, container homes, treehouses) care vor sa iasa din dependenta de platforme",
  "Agentii de turism locale si proiecte de destinatii turistice care vor sa-si optimizeze prezenta digitala",
  "Proprietari care nu au echipa interna de marketing si vor un partener care preia totul",
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
          Pentru cine este aceasta solutie de marketing in turism?
        </h2>

        <p className="mx-auto mb-10 max-w-2xl text-center text-lg leading-relaxed text-muted-foreground">
          Serviciul nostru de audit si marketing turistic este destinat:
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
