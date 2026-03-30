import { ClipboardList, Lightbulb, Rocket } from "lucide-react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const STEPS = [
  {
    icon: ClipboardList,
    badge: "Pasul 1",
    title: "Audit gratuit",
    description:
      "In aproximativ 5 minute completezi formularul. Primesti un raport personalizat fara acces la datele tale interne. Analizam date publice si folosim AI pentru a identifica rapid ce pierzi si ce poti imbunatati. Acest prim pas te introduce in solutia noastra de marketing pentru turism.",
    highlighted: true,
  },
  {
    icon: Lightbulb,
    badge: "Pasul 2",
    title: "Consultanta strategica",
    description:
      "Dupa audit, discutam strategia ta de marketing turistic: definim prioritati, obiective si canale - de la SEO pentru turism la campanii de promovare, social media si email marketing. Totul adaptat la tipul tau de proprietate si la sezonalitate.",
    highlighted: false,
  },
  {
    icon: Rocket,
    badge: "Pasul 3",
    title: "Implementare & crestere",
    description:
      "Daca decizi sa continuam impreuna, preluam implementarea: campanii de promovare turistica, optimizare continua, monitorizare si raportare transparenta. Tu te ocupi de oaspeti, noi de vizibilitate si rezervari directe.",
    highlighted: false,
  },
] as const;

export function ProcessSection() {
  return (
    <section aria-labelledby="process-heading" className="bg-white">
      <div className="mx-auto max-w-[1200px] px-4 py-16 sm:px-6 md:py-20">
        <h2
          id="process-heading"
          className="mb-10 text-center font-display text-[clamp(1.5rem,3vw,2rem)] font-bold tracking-tight text-foreground"
        >
          Ce face auditul nostru + ce urmeaza: pasi simpli pentru promovare turistica
        </h2>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {STEPS.map((step) => (
            <Card
              key={step.title}
              className={
                step.highlighted
                  ? "border-2 border-primary bg-brand-teal-lightest/30"
                  : "border-border/50"
              }
            >
              <CardHeader>
                <Badge
                  variant={step.highlighted ? "default" : "secondary"}
                  className="mb-2 w-fit"
                >
                  {step.badge}
                </Badge>
                <div className="mb-1 flex size-10 items-center justify-center rounded-xl bg-brand-teal-lightest">
                  <step.icon className="size-5 text-primary" />
                </div>
                <CardTitle className="text-base">{step.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-sm leading-relaxed">
                  {step.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
