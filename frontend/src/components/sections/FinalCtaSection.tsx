import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

export function FinalCtaSection() {
  return (
    <section
      aria-labelledby="final-cta-heading"
      className="bg-brand-teal-darkest"
    >
      <div className="mx-auto max-w-[1200px] px-4 py-16 sm:px-6 md:py-20">
        <div className="mx-auto flex max-w-2xl flex-col items-center gap-6 text-center">
          <h2
            id="final-cta-heading"
            className="font-display text-[clamp(1.5rem,3vw,2.25rem)] font-bold tracking-tight text-white"
          >
            Esti gata sa transformi prezenta digitala a afacerii tale de turism?
          </h2>

          <p className="text-lg leading-relaxed text-brand-teal-lighter">
            Solicita auditul digital gratuit si afla exact unde pierzi
            vizibilitate si rezervari directe. Raport personalizat, fara
            obligatii, in 30-90 de minute.
          </p>

          <Button
            asChild
            size="lg"
            className="bg-gradient-cta text-foreground font-semibold shadow-lg hover:shadow-xl transition-shadow"
          >
            <Link href="/marketing-pentru-turism#audit-form">
              Solicită auditul gratuit
              <ArrowRight className="size-4" />
            </Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
