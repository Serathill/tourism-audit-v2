import { Bot, Zap, ShieldCheck, Users, ExternalLink } from "lucide-react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { BRAND } from "@/lib/constants";

const DIFFERENTIATORS = [
  {
    icon: Bot,
    title: "Singura analiză cu AI din turismul românesc",
    description:
      "Folosim Gemini Deep Research Pro pentru a genera audituri cuprinzătoare. Niciun competitor din piață nu oferă acest nivel de automatizare.",
  },
  {
    icon: Zap,
    title: "Raport în 30-90 de minute",
    description:
      "În timp ce competiția livrează audituri manuale în zile sau săptămâni, AI-ul nostru analizează prezența ta online și livrează raportul pe email.",
  },
  {
    icon: ShieldCheck,
    title: "Fără acces la date interne",
    description:
      "Analizăm exclusiv informații publice: Google, platforme de booking, social media, recenzii. Nu cerem niciodată parole sau acces la conturile tale.",
  },
  {
    icon: Users,
    title: "Echipă cu experiență Deloitte",
    description:
      "Alexandru Mihailă, CMO ex-Deloitte, coordonează strategia. Petru și Nicu aduc experiență în dezvoltare de business și tehnologie AI.",
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
          className="mb-10 text-center font-display text-[clamp(1.5rem,3vw,2rem)] font-bold tracking-tight text-foreground"
        >
          De ce să alegi marketing digital pentru turism cu noi
        </h2>

        <div className="grid gap-6 sm:grid-cols-2">
          {DIFFERENTIATORS.map((item) => (
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
