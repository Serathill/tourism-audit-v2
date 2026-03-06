import { TrendingUp, Zap, ShieldCheck, Users, ExternalLink } from "lucide-react";
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
    title: "Nu mai pierzi rezervări directe",
    description:
      "Reducem dependența de platformele care percep comisioane mari.",
  },
  {
    icon: Zap,
    title: "Marketing care funcționează",
    description:
      "Implementăm o strategie personalizată care atrage clienții ideali pentru tine.",
  },
  {
    icon: ShieldCheck,
    title: "Timp și energie salvate",
    description:
      "Ne ocupăm noi de complexitatea marketingului digital. Tu te concentrezi pe oaspeți.",
  },
  {
    icon: Users,
    title: "Un partener, nu un furnizor",
    description:
      "Oferim transparență totală și suport constant pentru a-ți atinge obiectivele.",
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
          Parteneriatul cu noi înseamnă rezultate
        </h2>

        <p className="mx-auto mb-10 max-w-2xl text-center text-muted-foreground">
          Totul începe cu auditul și o discuție de follow-up, ambele 100%
          gratuite. Primești o analiză valoroasă și recomandări concrete,
          fără niciun cost sau obligație.
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
