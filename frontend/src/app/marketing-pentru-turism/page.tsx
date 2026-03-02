import type { Metadata } from "next";
import { HeroSection } from "@/components/sections/HeroSection";
import { AudienceSection } from "@/components/sections/AudienceSection";
import { ProcessSection } from "@/components/sections/ProcessSection";
import { WhyUsSection } from "@/components/sections/WhyUsSection";
import { FinalCtaSection } from "@/components/sections/FinalCtaSection";
import { SectionDivider } from "@/components/layout/SectionDivider";

export const metadata: Metadata = {
  title: "Marketing pentru turism & audit digital gratuit | DeviDevs Agency",
  description:
    "Primește un audit digital gratuit pentru pensiunea sau unitatea ta de cazare. Analizăm prezența online folosind doar informații publice. Rezultate în 30-90 minute.",
  alternates: {
    canonical: "/marketing-pentru-turism",
  },
};

// ISR: revalidate every 7 days
export const revalidate = 604800;

export default function MarketingPentruTurismPage() {
  return (
    <>
      <HeroSection />
      <SectionDivider />
      <AudienceSection />
      <SectionDivider />
      <ProcessSection />
      <SectionDivider />
      <WhyUsSection />
      <SectionDivider />
      <FinalCtaSection />
    </>
  );
}
