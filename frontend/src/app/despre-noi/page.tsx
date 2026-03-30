import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowRight, ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { TEAM_MEMBERS, BRAND } from "@/lib/constants";

const siteUrl =
  process.env.NEXT_PUBLIC_SITE_URL || "https://audit-turism.ro";

export const metadata: Metadata = {
  title: "Despre noi",
  description:
    "Echipa de marketing digital din spatele Audit Digital Turism. Alexandru Mihailă (ex-Deloitte), Petru Constantin (CEO) și Nicu Constantin (CTO).",
  alternates: {
    canonical: "/despre-noi",
  },
  openGraph: {
    title: "Despre noi | Audit Digital Turism",
    description:
      "Echipa de marketing digital din spatele Audit Digital Turism. Alexandru Mihailă, Petru Constantin și Nicu Constantin.",
    type: "website",
    url: `${siteUrl}/despre-noi`,
    images: [
      {
        url: "/preview-image.png",
        width: 1200,
        height: 630,
        alt: "Echipa Audit Digital Turism",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Despre noi | Audit Digital Turism",
    description: "Echipa de marketing digital din spatele Audit Digital Turism.",
    images: ["/preview-image.png"],
  },
};

export const revalidate = 604800; // 7 days

export default function DespreNoiPage() {
  return (
    <div className="mx-auto max-w-[1200px] px-4 py-12 sm:px-6 md:py-16">
      {/* Page header */}
      <div className="mb-10 text-center">
        <h1 className="font-display text-[clamp(1.75rem,4vw,2.5rem)] font-bold tracking-tight text-foreground">
          Despre noi
        </h1>
        <p className="mt-3 text-lg text-muted-foreground">
          Echipa de marketing digital din spatele {BRAND.name}
        </p>
      </div>

      {/* Team cards */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {TEAM_MEMBERS.map((member) => (
          <Card key={member.name} className="overflow-hidden">
            <CardHeader className="items-center justify-items-center text-center">
              <div className="relative mb-2 size-24 overflow-hidden rounded-full border-2 border-primary">
                <Image
                  src={member.image}
                  alt={member.name}
                  fill
                  sizes="96px"
                  className="object-cover object-top"
                />
              </div>
              <CardTitle className="text-lg">{member.name}</CardTitle>
              <CardDescription className="font-medium text-primary">
                {member.role}
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-sm text-muted-foreground">
                {member.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Parent brand card */}
      <div className="mt-12">
        <Card className="mx-auto max-w-lg border-border/50 bg-muted/30">
          <CardContent className="flex flex-col items-center gap-3 pt-6 text-center">
            <p className="text-sm text-muted-foreground">{BRAND.tagline}</p>
            <p className="font-display text-lg font-bold text-foreground">
              {BRAND.parentName}
            </p>
            <p className="text-sm text-muted-foreground">
              Soluții de marketing digital pentru turism, ecommerce și health
            </p>
            <a
              href={BRAND.parentUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-sm font-medium text-primary transition-colors hover:text-brand-teal-dark"
            >
              Vizitează {BRAND.parentUrl.replace("https://", "")}
              <ExternalLink className="size-3.5" />
            </a>
          </CardContent>
        </Card>
      </div>

      {/* CTA */}
      <div className="mt-12 text-center">
        <p className="mb-4 text-muted-foreground">
          Vrei să afli cum te putem ajuta?
        </p>
        <Button
          asChild
          size="lg"
          className="bg-gradient-cta text-foreground font-semibold shadow-md"
        >
          <Link href="/audit">
            Solicită auditul gratuit
            <ArrowRight className="size-4" />
          </Link>
        </Button>
      </div>
    </div>
  );
}
