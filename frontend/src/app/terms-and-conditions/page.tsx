import type { Metadata } from "next";
import Link from "next/link";
import { BRAND } from "@/lib/constants";

export const metadata: Metadata = {
  title: "Termeni și condiții",
  description:
    "Termenii și condițiile de utilizare pentru Audit Digital Turism, un serviciu de la DeviDevs Agency.",
  alternates: {
    canonical: "/terms-and-conditions",
  },
};

export const revalidate = 2592000; // 30 days

export default function TermsAndConditionsPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 md:py-16">
      {/* Breadcrumb */}
      <nav aria-label="Breadcrumb" className="mb-6 text-sm text-muted-foreground">
        <Link href="/marketing-pentru-turism" className="hover:text-primary transition-colors">
          Acasă
        </Link>
        <span className="mx-2">›</span>
        <span>Termeni și condiții</span>
      </nav>

      <h1 className="mb-8 font-display text-[clamp(1.75rem,4vw,2.5rem)] font-bold tracking-tight text-foreground">
        Termeni și condiții
      </h1>

      <div className="prose prose-slate max-w-none [&_h2]:font-display [&_h2]:text-xl [&_h2]:font-bold [&_h2]:mt-8 [&_h2]:mb-4 [&_p]:leading-relaxed [&_p]:text-muted-foreground [&_p]:mb-4 [&_ul]:list-disc [&_ul]:pl-6 [&_ul]:mb-4 [&_li]:text-muted-foreground [&_li]:mb-1">
        <p>
          Ultima actualizare: februarie 2026
        </p>

        <h2>1. Descrierea serviciului</h2>
        <p>
          {BRAND.name} este un serviciu gratuit de audit digital oferit de{" "}
          {BRAND.parentName}. Serviciul analizează prezența online a unităților
          de cazare din România folosind exclusiv informații disponibile public.
        </p>

        <h2>2. Acceptarea termenilor</h2>
        <p>
          Prin utilizarea serviciului și completarea formularului de audit,
          accepți acești termeni și condiții. Dacă nu ești de acord, te rugăm
          să nu folosești serviciul.
        </p>

        <h2>3. Serviciul de audit</h2>
        <ul>
          <li>Auditul este generat automat folosind inteligență artificială</li>
          <li>Rezultatele sunt orientative și nu constituie consultanță profesională garantată</li>
          <li>Timpul de livrare estimat este de 30-90 de minute, dar poate varia</li>
          <li>Ne rezervăm dreptul de a refuza cereri care nu respectă termenii de utilizare</li>
        </ul>

        <h2>4. Limitarea răspunderii</h2>
        <p>
          {BRAND.parentName} nu garantează acuratețea 100% a rezultatelor
          auditului. Raportul este generat pe baza informațiilor disponibile
          public la momentul analizei. Deciziile luate pe baza raportului sunt
          responsabilitatea exclusivă a utilizatorului.
        </p>

        <h2>5. Proprietate intelectuală</h2>
        <p>
          Conținutul site-ului, inclusiv textele, designul și funcționalitățile,
          este proprietatea {BRAND.parentName}. Raportul de audit generat poate
          fi utilizat liber de destinatar.
        </p>

        <h2>6. Utilizarea acceptabilă</h2>
        <p>Te angajezi să:</p>
        <ul>
          <li>Furnizezi informații corecte în formularul de audit</li>
          <li>Nu folosești serviciul pentru spam sau în scopuri malițioase</li>
          <li>Nu încerci să compromiți securitatea sau funcționarea serviciului</li>
        </ul>

        <h2>7. Modificări</h2>
        <p>
          Ne rezervăm dreptul de a modifica acești termeni. Modificările intră
          în vigoare la publicarea pe această pagină.
        </p>

        <h2>8. Legea aplicabilă</h2>
        <p>
          Acești termeni sunt guvernați de legislația română. Orice dispută va
          fi soluționată de instanțele competente din România.
        </p>

        <h2>9. Contact</h2>
        <p>
          Pentru întrebări:
          <br />
          {BRAND.parentName}
          <br />
          Email:{" "}
          <a href={`mailto:${BRAND.email}`} className="text-primary hover:underline">
            {BRAND.email}
          </a>
        </p>
      </div>
    </div>
  );
}
