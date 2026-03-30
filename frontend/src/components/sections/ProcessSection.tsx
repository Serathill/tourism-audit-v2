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
      "Completezi formularul in 2 minute. In maximum 90 de minute primesti pe email un raport detaliat cu ce te costa si ce poti imbunatati. Analizam doar informatii publice.",
    highlighted: true,
  },
  {
    icon: Lightbulb,
    badge: "Pasul 2",
    title: "Consultanta strategica",
    description:
      "Programam o discutie scurta, tot gratuita, in care iti explicam raportul si raspundem la intrebari. Fara presiune.",
    highlighted: false,
  },
  {
    icon: Rocket,
    badge: "Pasul 3",
    title: "Implementare & crestere",
    description:
      "Poti implementa singur recomandarile sau ne ocupam noi. Tu te concentrezi pe oaspeti, noi pe vizibilitate.",
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
          Cum functioneaza
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
