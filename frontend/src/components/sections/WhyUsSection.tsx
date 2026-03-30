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
    title: "Afli concret ce te costa",
    description:
      "Nu primesti sfaturi vagi. Raportul iti arata exact unde pierzi vizibilitate si ce poti face, cu impact estimat in rezervari.",
  },
  {
    icon: Zap,
    title: "Gata in 90 de minute",
    description:
      "Completezi formularul in 2 minute. Raportul ajunge pe email in maximum 90 de minute. Fara apeluri, fara asteptare.",
  },
  {
    icon: ShieldCheck,
    title: "Bazat pe date reale",
    description:
      "Analizam peste 60 de surse publice: Google, Booking, TripAdvisor, social media, site-ul tau. Nu ghicim, verificam.",
  },
  {
    icon: Users,
    title: "Facut de o echipa care intelege turismul",
    description:
      "Stim ce inseamna sezonalitate, extrasezon si dependenta de platforme. Nu suntem o agentie generica.",
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
          De ce functioneaza acest audit
        </h2>

        <p className="mx-auto mb-10 max-w-2xl text-center text-muted-foreground">
          Auditul si discutia de follow-up sunt 100% gratuite.
          Primesti recomandari concrete, fara obligatii.
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
