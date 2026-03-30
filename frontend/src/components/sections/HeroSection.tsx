import Image from "next/image";
import Link from "next/link";
import { ArrowRight, CheckCircle, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { TeamStrip } from "@/components/trust/TeamStrip";
import { TrustBadge } from "@/components/trust/TrustBadge";
import { FormWizardClient } from "@/components/form/FormWizardClient";

export function HeroSection() {
  const meetingLink = process.env.MEETING_LINK;

  return (
    <section
      aria-labelledby="hero-heading"
      className="relative overflow-hidden"
    >
      {/* Background image */}
      <Image
        src="/hero-pensiune.webp"
        alt=""
        fill
        priority
        className="object-cover"
        sizes="100vw"
      />
      {/* Overlay for text readability */}
      <div className="absolute inset-0 bg-white/80 backdrop-blur-[2px]" />

      <div className="relative mx-auto max-w-[1200px] px-4 py-12 sm:px-6 md:py-16 lg:py-20">
        <div className="grid items-center gap-10 lg:grid-cols-[1.2fr_1fr] lg:gap-16">
          {/* Left column — text content */}
          <div className="flex flex-col gap-6">
            <h1
              id="hero-heading"
              className="font-display text-[clamp(1.75rem,5vw,3rem)] font-extrabold leading-[1.1] tracking-tight text-foreground"
            >
              Marketing pentru turism &amp; audit digital gratuit pentru unitati de cazare
            </h1>

            <p className="text-lg font-medium leading-snug text-foreground/80 sm:text-xl">
              Vecinii tai au plin in weekend. Tu de ce nu?
            </p>

            <p className="max-w-xl text-lg leading-relaxed text-muted-foreground">
              In 30 de minute afli exact ce te costa vizibilitatea slaba online
              si ce poti face concret, incepand de azi. Nu cerem acces la
              datele tale.
            </p>

            <TeamStrip />

            <p className="inline-flex items-center gap-1.5 text-sm text-muted-foreground">
              <CheckCircle className="size-4 text-primary" />
              <span className="font-medium text-foreground">15+</span> proprietati analizate in Romania
            </p>

            {/* Mobile CTA (visible only on mobile/tablet where form isn't side-by-side) */}
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center lg:hidden">
              <Button
                asChild
                size="lg"
                className="bg-gradient-cta text-foreground font-semibold shadow-md hover:shadow-lg transition-shadow"
              >
                <Link href="#audit-form">
                  Solicită auditul gratuit
                  <ArrowRight className="size-4" />
                </Link>
              </Button>
              <span className="inline-flex items-center gap-1.5 text-sm text-muted-foreground">
                <Clock className="size-3.5" />
                Completează în 2 minute
              </span>
            </div>
          </div>

          {/* Right column — form wizard */}
          <div id="audit-form" className="scroll-mt-20">
            <div className="rounded-2xl border border-border bg-white p-6 shadow-sm sm:p-8 sm:shadow-md">
              <FormWizardClient meetingLink={meetingLink} />
            </div>

            {/* Trust badge below form */}
            <div className="mt-4 flex justify-center">
              <TrustBadge />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
