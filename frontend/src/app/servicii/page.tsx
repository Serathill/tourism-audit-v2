import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight, ClipboardList, Lightbulb, Rocket } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";

export const metadata: Metadata = {
  title: "Servicii",
  description:
    "Trei pași simpli de la audit la creștere: audit digital gratuit, consultanță strategică (de la 149 RON/lună), implementare completă (de la 699 RON/lună).",
  alternates: {
    canonical: "/servicii",
  },
  openGraph: {
    title: "Servicii | Audit Digital Turism",
    type: "website",
    url: "https://audit.devidevs.com/servicii",
    images: [
      {
        url: "/preview-image.png",
        width: 1200,
        height: 630,
        alt: "Servicii Audit Digital Turism",
      },
    ],
  },
  twitter: { card: "summary_large_image", images: ["/preview-image.png"] },
};

export const revalidate = 604800; // 7 days

const SERVICES = [
  {
    icon: ClipboardList,
    title: "Audit digital gratuit",
    price: "GRATUIT",
    priceColor: "text-[var(--success)]",
    highlighted: true,
    features: [
      "Analiză completă a prezenței online",
      "Raport cu recomandări personalizate",
      "Benchmark competitiv",
      "Livrare în 30-90 de minute",
    ],
    cta: { label: "Solicită auditul gratuit", href: "/audit" },
    ctaPrimary: true,
  },
  {
    icon: Lightbulb,
    title: "Consultanță strategică",
    price: "de la 149 RON/lună",
    priceColor: "text-foreground",
    highlighted: false,
    features: [
      "Sesiune strategică lunară",
      "Plan de acțiune prioritizat",
      "Suport pe email",
      "Raportare lunară",
    ],
    cta: { label: "Programează consultanță", href: "/audit" },
    ctaPrimary: false,
  },
  {
    icon: Rocket,
    title: "Implementare & creștere",
    price: "de la 699 RON/lună",
    priceColor: "text-foreground",
    highlighted: false,
    features: [
      "Implementare completă",
      "Google Ads + Social Media",
      "Optimizare website",
      "Raportare săptămânală",
    ],
    cta: { label: "Discută cu noi", href: "/audit" },
    ctaPrimary: false,
  },
] as const;

export default function ServiciiPage() {
  return (
    <div className="mx-auto max-w-[1200px] px-4 py-12 sm:px-6 md:py-16">
      {/* Page header */}
      <div className="mb-10 text-center">
        <h1 className="font-display text-[clamp(1.75rem,4vw,2.5rem)] font-bold tracking-tight text-foreground">
          Servicii
        </h1>
        <p className="mt-3 text-lg text-muted-foreground">
          Trei pași simpli de la audit la creștere
        </p>
      </div>

      {/* Service cards */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
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
                  <Link href={service.cta.href}>
                    {service.cta.label}
                    <ArrowRight className="size-4" />
                  </Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
