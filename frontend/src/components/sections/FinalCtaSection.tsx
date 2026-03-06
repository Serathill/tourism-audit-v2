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
            Ești gata să-ți crești vizibilitatea și să atragi mai mulți
            clienți?
          </h2>

          <p className="text-lg leading-relaxed text-brand-teal-lighter">
            Solicită acum auditul digital gratuit și începe să descoperi
            potențialul real al unității tale de cazare!
          </p>

          <Button
            asChild
            size="lg"
            className="bg-gradient-cta text-foreground font-semibold shadow-lg hover:shadow-xl transition-shadow"
          >
            <Link href="/audit">
              Solicită auditul gratuit
              <ArrowRight className="size-4" />
            </Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
