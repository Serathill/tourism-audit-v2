import type { Metadata } from "next";
import Link from "next/link";
import {
  ArrowRight,
  ClipboardList,
  Lightbulb,
  PenTool,
  Globe,
  Bot,
  Target,
  Cpu,
  Clock,
  HandCoins,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";

const siteUrl =
  process.env.NEXT_PUBLIC_SITE_URL || "https://audit-turism.ro";

export const metadata: Metadata = {
  title: "Servicii de marketing digital pentru turism",
  description:
    "De la audit digital gratuit la implementare completa: strategie de marketing turistic, content marketing, campanii digitale, optimizare website si automatizare cu AI. Preturi personalizate.",
  alternates: {
    canonical: "/servicii",
  },
  openGraph: {
    title: "Servicii de marketing digital pentru turism | Audit Digital Turism",
    description:
      "Servicii complete de marketing digital pentru pensiuni, hoteluri si unitati de cazare din Romania. Audit gratuit, strategie, campanii si automatizare.",
    type: "website",
    url: `${siteUrl}/servicii`,
    images: [
      {
        url: "/preview-image.png",
        width: 1200,
        height: 630,
        alt: "Servicii Audit Digital Turism",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Servicii de marketing digital pentru turism | Audit Digital Turism",
    description:
      "Servicii complete de marketing digital pentru turism. Audit gratuit, strategie, campanii si automatizare.",
    images: ["/preview-image.png"],
  },
};

export const revalidate = 604800; // 7 days

const SERVICES = [
  {
    icon: ClipboardList,
    title: "Audit digital gratuit",
    price: "GRATUIT",
    priceColor: "text-[var(--success)]",
    highlighted: true,
    description:
      "Analizam prezenta ta online folosind doar informatii publice si AI. Primesti un raport detaliat cu recomandari concrete in 30-90 de minute.",
    features: [
      "Analiza completa a prezentei online",
      "Raport cu recomandari personalizate",
      "Benchmark competitiv in nisa ta",
      "Livrare in 30-90 de minute",
      "Fara acces la date interne",
    ],
    cta: {
      label: "Solicita auditul gratuit",
      href: "/marketing-pentru-turism#audit-form",
    },
    ctaPrimary: true,
  },
  {
    icon: Lightbulb,
    title: "Strategie de marketing digital",
    price: "Preturi personalizate",
    priceColor: "text-foreground",
    highlighted: false,
    description:
      "Audit complet + strategie personalizata + planificare campanii, accelerate cu AI. Definim impreuna obiectivele, canalele si pasii concreti pentru cresterea rezervarilor directe.",
    features: [
      "Audit digital aprofundat",
      "Strategie de marketing turistic personalizata",
      "Planificare campanii multi-canal",
      "Definitie KPI-uri si obiective",
      "Analiza competitiva cu AI",
      "Sesiuni de consultanta strategica",
    ],
    forWhom:
      "Proprietari de unitati de cazare care vor sa creasca digital dar nu stiu de unde sa inceapa.",
    cta: {
      label: "Programeaza o consultatie gratuita",
      href: "https://meetings-eu1.hubspot.com/alexandru-damian?uuid=1480d7cd-ef6e-4784-b86a-ac2228e4b749",
    },
    ctaPrimary: false,
  },
  {
    icon: PenTool,
    title: "Content marketing & campanii digitale",
    price: "Preturi personalizate",
    priceColor: "text-foreground",
    highlighted: false,
    description:
      "Campanii de content si advertising bazate pe date, cu suport AI. De la postari pe social media la Google Ads si SEO - totul adaptat pe sezonalitatea turismului.",
    features: [
      "Strategie de continut per canal",
      "Calendar editorial adaptat pe sezoane",
      "Copywriting cu suport AI",
      "Google Ads & Social Media Ads",
      "SEO & keyword research turism",
      "Analiza si raportare performanta",
    ],
    forWhom:
      "Afaceri din turism care au nevoie de prezenta digitala constanta dar nu au echipa interna.",
    cta: {
      label: "Cere o propunere",
      href: "https://meetings-eu1.hubspot.com/alexandru-damian?uuid=1480d7cd-ef6e-4784-b86a-ac2228e4b749",
    },
    ctaPrimary: false,
  },
  {
    icon: Globe,
    title: "Optimizare website",
    price: "Preturi personalizate",
    priceColor: "text-foreground",
    highlighted: false,
    description:
      "Optimizam site-ul tau pentru performanta, viteza si conversie. De la SEO tehnic la experienta utilizatorului - ca vizitatorii sa devina oaspeti.",
    features: [
      "Audit tehnic SEO complet",
      "Optimizare viteza si performanta",
      "Imbunatatire experienta utilizator (UX)",
      "Optimizare pagini pentru conversie (rezervari)",
      "Compatibilitate mobile",
      "Monitorizare si raportare",
    ],
    forWhom:
      "Unitati de cazare care au site dar nu primesc rezervari de pe el.",
    cta: {
      label: "Discuta cu noi",
      href: "https://meetings-eu1.hubspot.com/alexandru-damian?uuid=1480d7cd-ef6e-4784-b86a-ac2228e4b749",
    },
    ctaPrimary: false,
  },
  {
    icon: Bot,
    title: "Automatizare marketing cu AI",
    price: "Preturi personalizate",
    priceColor: "text-foreground",
    highlighted: false,
    description:
      "Reducem timpul de executie al marketingului tau cu pana la 80%. Automatizam procesele repetitive ca tu sa te concentrezi pe oaspeti.",
    features: [
      "Audit procese de marketing existente",
      "Design fluxuri automate (email, social, follow-up)",
      "Integrare instrumente si platforme",
      "Configurare agenti AI",
      "Training echipa",
    ],
    forWhom:
      "Proprietari sau manageri care pierd timp pe taskuri repetitive de marketing.",
    cta: {
      label: "Discuta cu noi",
      href: "https://meetings-eu1.hubspot.com/alexandru-damian?uuid=1480d7cd-ef6e-4784-b86a-ac2228e4b749",
    },
    ctaPrimary: false,
  },
];

const WHY_US = [
  {
    icon: Target,
    title: "Specializati pe turism si cazari inedite",
    description:
      "Nu suntem o agentie generica. Intelegem sezonalitatea, comportamentul turistilor si provocarile specifice proprietarilor de tiny houses, pensiuni boutique si cazari unice din Romania.",
  },
  {
    icon: Cpu,
    title: "Tehnologie proprie cu AI",
    description:
      "Am construit instrumente interne care accelereaza analiza, crearea de continut si optimizarea campaniilor.",
  },
  {
    icon: Clock,
    title: "10+ ani experienta",
    description:
      "Experienta in marketing digital, consultanta si antreprenoriat.",
  },
  {
    icon: HandCoins,
    title: "Preturi personalizate",
    description:
      "Fiecare oferta e adaptata pe nevoile si bugetul tau. Fara pachete generice.",
  },
];

export default function ServiciiPage() {
  return (
    <div className="mx-auto max-w-[1200px] px-4 py-12 sm:px-6 md:py-16">
      {/* Page header */}
      <div className="mb-10 text-center">
        <h1 className="font-display text-[clamp(1.75rem,4vw,2.5rem)] font-bold tracking-tight text-foreground">
          Servicii de marketing digital pentru turism
        </h1>
        <p className="mt-3 text-lg text-muted-foreground">
          De la audit gratuit la implementare completa - tot ce ai nevoie pentru
          mai multe rezervari directe
        </p>
      </div>

      {/* Service cards - first row: 1 highlighted + 1 */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {SERVICES.map((service) => (
          <Card
            key={service.title}
            className={
              service.highlighted
                ? "border-2 border-primary relative"
                : "border-border/50"
            }
          >
            {service.highlighted && (
              <Badge className="absolute -top-3 left-6 bg-primary text-white">
                Recomandat
              </Badge>
            )}
            <CardHeader>
              <div className="mb-2 flex size-10 items-center justify-center rounded-xl bg-brand-teal-lightest">
                <service.icon className="size-5 text-primary" />
              </div>
              <CardTitle className="text-lg">{service.title}</CardTitle>
              <CardDescription
                className={`text-base font-semibold ${service.priceColor}`}
              >
                {service.price}
              </CardDescription>
            </CardHeader>
            <CardContent className="flex flex-1 flex-col gap-4">
              <p className="text-sm leading-relaxed text-muted-foreground">
                {service.description}
              </p>
              <ul className="flex flex-col gap-2">
                {service.features.map((feature) => (
                  <li
                    key={feature}
                    className="flex items-start gap-2 text-sm text-muted-foreground"
                  >
                    <span className="mt-0.5 text-primary">•</span>
                    {feature}
                  </li>
                ))}
              </ul>
              {service.forWhom && (
                <p className="text-xs italic text-muted-foreground">
                  Pentru: {service.forWhom}
                </p>
              )}
              <div className="mt-auto pt-2">
                <Button
                  asChild
                  className={
                    service.ctaPrimary
                      ? "w-full bg-gradient-cta text-foreground font-semibold shadow-md"
                      : "w-full"
                  }
                  variant={service.ctaPrimary ? "default" : "outline"}
                >
                  <Link
                    href={service.cta.href}
                    {...(service.cta.href.startsWith("http") ? { target: "_blank", rel: "noopener noreferrer" } : {})}
                  >
                    {service.cta.label}
                    <ArrowRight className="size-4" />
                  </Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* De ce noi */}
      <div className="mt-16">
        <h2 className="mb-8 text-center font-display text-[clamp(1.5rem,3vw,2rem)] font-bold tracking-tight text-foreground">
          De ce noi
        </h2>
        <div className="grid gap-6 sm:grid-cols-2">
          {WHY_US.map((item) => (
            <div
              key={item.title}
              className="flex items-start gap-4 rounded-lg border border-border/50 bg-muted/30 p-5"
            >
              <div className="flex size-10 shrink-0 items-center justify-center rounded-xl bg-brand-teal-lightest">
                <item.icon className="size-5 text-primary" />
              </div>
              <div>
                <h3 className="font-semibold text-foreground">{item.title}</h3>
                <p className="mt-1 text-sm leading-relaxed text-muted-foreground">
                  {item.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* CTA final */}
      <div className="mt-16 text-center">
        <p className="mb-4 text-lg text-muted-foreground">
          Consultanta initiala e gratuita. Spune-ne despre proprietatea ta si
          primesti un audit digital + recomandari personalizate, fara obligatii.
        </p>
        <Button
          asChild
          size="lg"
          className="bg-gradient-cta text-foreground font-semibold shadow-md"
        >
          <Link href="/marketing-pentru-turism#audit-form">
            Programeaza audit gratuit
            <ArrowRight className="size-4" />
          </Link>
        </Button>
      </div>
    </div>
  );
}
