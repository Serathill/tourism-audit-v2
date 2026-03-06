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
      "În aproximativ 5 minute, primești un raport complet, fără niciun efort din partea ta și fără să ne dai acces la date interne. Folosim inteligența artificială și date publice pentru a identifica rapid nevoile și oportunitățile de creștere.",
    highlighted: true,
  },
  {
    icon: Lightbulb,
    badge: "Pasul 2",
    title: "Consultanță strategică",
    description:
      "După audit, îți oferim o sesiune de consultanță dedicată în care discutăm situația ta actuală și îți propunem o strategie digitală clară, adaptată obiectivelor tale, cu pași concreți și priorități clare.",
    highlighted: false,
  },
  {
    icon: Rocket,
    badge: "Pasul 3",
    title: "Implementare & creștere",
    description:
      "Te ajutăm să pui în practică soluțiile recomandate. Beneficiezi de implementare completă, monitorizare a rezultatelor și suport constant. Tu te ocupi de oaspeți, noi de vizibilitate.",
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
          Pașii simpli pentru afacerea ta
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
