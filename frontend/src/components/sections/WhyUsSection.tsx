import { TrendingUp, Zap, ShieldCheck, Users, Layers, ExternalLink } from "lucide-react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { BRAND } from "@/lib/constants";

const BENEFITS = [
  {
    icon: TrendingUp,
    title: "Crestere reala a rezervarilor directe",
    description:
      "Proprietatile cu care lucram vad in medie +85% rezervari directe si +150% vizibilitate online in primele 6 luni.",
  },
  {
    icon: Zap,
    title: "Reducerea dependentei de platforme",
    description:
      "Strategii de marketing turistic care aduc trafic direct pe site-ul tau, nu prin Booking sau Airbnb cu comisioane de 15-25%.",
  },
  {
    icon: ShieldCheck,
    title: "Timp si energie salvate",
    description:
      "Ne ocupam noi de complexitatea marketingului digital. Tu te concentrezi pe experienta oaspetilor - care e motivul pentru care te aleg.",
  },
  {
    icon: Users,
    title: "Un partener, nu un furnizor",
    description:
      "Oferim transparenta totala, raportare clara si suport constant. Intelegem sezonalitatea turismului si adaptam strategia in consecinta.",
  },
  {
    icon: Layers,
    title: "Servicii integrate de marketing turistic",
    description:
      "De la strategie digitala si SEO la campanii de promovare, content marketing, optimizare website si automatizari - totul intr-un singur loc.",
  },
] as const;

export function WhyUsSection() {
  return (
    <section
      aria-labelledby="whyus-heading"
      className="bg-[var(--bg-secondary)]"
    >
      <div className="mx-auto max-w-[1200px] px-4 py-16 sm:px-6 md:py-20">
        <h2
          id="whyus-heading"
          className="mb-4 text-center font-display text-[clamp(1.5rem,3vw,2rem)] font-bold tracking-tight text-foreground"
        >
          De ce sa alegi marketing digital pentru turism cu noi
        </h2>

        <p className="mx-auto mb-10 max-w-2xl text-center text-muted-foreground">
          Totul incepe cu auditul si o discutie de follow-up, ambele 100%
          gratuite. Primesti o analiza valoroasa si recomandari concrete,
          fara niciun cost sau obligatie.
        </p>

        <div className="grid gap-6 sm:grid-cols-2">
          {BENEFITS.map((item) => (
            <Card
              key={item.title}
              className="border-border/50 bg-white transition-shadow hover:shadow-md"
            >
              <CardHeader>
                <div className="mb-2 flex size-10 items-center justify-center rounded-xl bg-brand-teal-lightest">
                  <item.icon className="size-5 text-primary" />
                </div>
                <CardTitle className="text-base">{item.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-sm leading-relaxed">
                  {item.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Parent brand endorsement */}
        <div className="mt-10 text-center">
          <p className="text-sm text-muted-foreground">
            Un serviciu de la{" "}
            <a
              href={BRAND.parentUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 font-medium text-primary transition-colors hover:text-brand-teal-dark"
            >
              {BRAND.parentName}
              <ExternalLink className="size-3" />
            </a>
          </p>
        </div>
      </div>
    </section>
  );
}
