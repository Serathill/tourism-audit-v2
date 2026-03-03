import type { Metadata } from "next";
import Link from "next/link";
import { BRAND } from "@/lib/constants";

export const metadata: Metadata = {
  title: "Politica de confidențialitate",
  description:
    "Politica de confidențialitate pentru Audit Digital Turism, un serviciu de la DeviDevs Agency.",
  alternates: {
    canonical: "/privacy-policy",
  },
  openGraph: {
    title: "Politica de confidențialitate | Audit Digital Turism",
    type: "website",
    url: "https://audit.devidevs.com/privacy-policy",
    images: [
      {
        url: "/preview-image.png",
        width: 1200,
        height: 630,
        alt: "Audit Digital Turism",
      },
    ],
  },
  twitter: { card: "summary_large_image", images: ["/preview-image.png"] },
};

export const revalidate = 2592000; // 30 days

export default function PrivacyPolicyPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 md:py-16">
      {/* Breadcrumb */}
      <nav aria-label="Breadcrumb" className="mb-6 text-sm text-muted-foreground">
        <Link href="/marketing-pentru-turism" className="hover:text-primary transition-colors">
          Acasă
        </Link>
        <span className="mx-2">›</span>
        <span>Politica de confidențialitate</span>
      </nav>

      <h1 className="mb-8 font-display text-[clamp(1.75rem,4vw,2.5rem)] font-bold tracking-tight text-foreground">
        Politica de confidențialitate
      </h1>

      <div className="prose prose-slate max-w-none [&_h2]:font-display [&_h2]:text-xl [&_h2]:font-bold [&_h2]:mt-8 [&_h2]:mb-4 [&_p]:leading-relaxed [&_p]:text-muted-foreground [&_p]:mb-4 [&_ul]:list-disc [&_ul]:pl-6 [&_ul]:mb-4 [&_li]:text-muted-foreground [&_li]:mb-1">
        <p>
          Ultima actualizare: februarie 2026
        </p>

        <h2>1. Introducere</h2>
        <p>
          {BRAND.name} (operat de {BRAND.parentName}) respectă
          confidențialitatea datelor tale. Această politică descrie ce date
          colectăm, cum le folosim și drepturile tale conform GDPR.
        </p>

        <h2>2. Date colectate</h2>
        <p>
          Colectăm doar datele pe care le furnizezi voluntar prin formularul
          de audit:
        </p>
        <ul>
          <li>Nume complet</li>
          <li>Adresa de email</li>
          <li>Numele proprietății de cazare</li>
          <li>Județul</li>
          <li>Informații opționale: URL website, link-uri social media, link-uri platforme booking, link Google My Business, descriere business</li>
        </ul>

        <h2>3. Scopul prelucrării</h2>
        <p>
          Datele tale sunt folosite exclusiv pentru:
        </p>
        <ul>
          <li>Generarea raportului de audit digital personalizat</li>
          <li>Trimiterea raportului pe email</li>
          <li>Comunicări ulterioare legate de audit (doar cu acordul tău)</li>
        </ul>

        <h2>4. Surse de date analizate</h2>
        <p>
          Auditul digital analizează exclusiv informații disponibile public:
          profiluri Google Business, listări pe platforme de booking, pagini de
          social media, performanța website-ului. Nu solicităm și nu accesăm
          niciodată date interne, parole sau conturi private.
        </p>

        <h2>5. Partajarea datelor</h2>
        <p>
          Nu vindem datele tale. Folosim următorii furnizori de servicii:
        </p>
        <ul>
          <li>Supabase (bază de date — UE)</li>
          <li>Resend (trimitere email)</li>
          <li>Google Analytics (analiză trafic — date anonimizate)</li>
          <li>Vercel (hosting — CDN global)</li>
        </ul>

        <h2>6. Păstrarea datelor</h2>
        <p>
          Datele tale sunt păstrate timp de maximum 24 de luni de la data
          colectării. Poți solicita ștergerea oricând.
        </p>

        <h2>7. Drepturile tale (GDPR)</h2>
        <p>
          Ai dreptul la: acces, rectificare, ștergere, restricționarea
          prelucrării, portabilitatea datelor și retragerea consimțământului.
          Pentru exercitarea acestor drepturi, contactează-ne la{" "}
          <a href={`mailto:${BRAND.email}`} className="text-primary hover:underline">
            {BRAND.email}
          </a>.
        </p>

        <h2>8. Cookies</h2>
        <p>
          Folosim cookies esențiale pentru funcționarea site-ului și cookies
          analitice (Google Analytics) doar cu consimțământul tău explicit.
          Poți gestiona preferințele tale de cookies oricând.
        </p>

        <h2>9. Contact</h2>
        <p>
          Pentru întrebări privind confidențialitatea datelor:
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
