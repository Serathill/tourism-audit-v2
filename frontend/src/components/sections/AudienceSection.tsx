import { Home, TreePine, Building2 } from "lucide-react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";

const PERSONAS = [
  {
    icon: Home,
    title: "Proprietari de pensiuni și case de vacanță",
    description:
      "Vrei să reduci dependența de Booking.com și să atragi turiști direct? Află ce oportunități de marketing digital pierzi în fiecare zi.",
  },
  {
    icon: TreePine,
    title: "Operatori de tiny houses, A-frames și eco-turism",
    description:
      "Piața ta crește rapid, dar vizibilitatea online face diferența. Descoperă dacă profilurile tale digitale sunt la nivelul competiției.",
  },
  {
    icon: Building2,
    title: "Agenții de turism și proiecte de dezvoltare turistică",
    description:
      "Identifică punctele slabe din strategia de marketing digital a clienților tăi sau a proiectului pe care îl coordonezi.",
  },
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
          className="mb-10 text-center font-display text-[clamp(1.5rem,3vw,2rem)] font-bold tracking-tight text-foreground"
        >
          Pentru cine este această soluție de marketing în turism?
        </h2>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {PERSONAS.map((persona) => (
            <Card
              key={persona.title}
              className="border-border/50 bg-white transition-shadow hover:shadow-md"
            >
              <CardHeader>
                <div className="mb-2 flex size-10 items-center justify-center rounded-xl bg-brand-teal-lightest">
                  <persona.icon className="size-5 text-primary" />
                </div>
                <CardTitle className="text-base">{persona.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-sm leading-relaxed">
                  {persona.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
