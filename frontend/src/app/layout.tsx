import type { Metadata } from "next";
import { Inter, Plus_Jakarta_Sans } from "next/font/google";
import { headers } from "next/headers";
import Script from "next/script";
import { Toaster } from "sonner";
import { PageHeader } from "@/components/layout/PageHeader";
import { PageFooter } from "@/components/layout/PageFooter";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin", "latin-ext"],
  display: "swap",
});

const plusJakartaSans = Plus_Jakarta_Sans({
  variable: "--font-plus-jakarta-sans",
  subsets: ["latin", "latin-ext"],
  display: "swap",
});

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://audit.devidevs.com";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "Audit Digital Gratuit pentru Turism | DeviDevs Agency",
    template: "%s | Audit Digital Turism",
  },
  description:
    "Primeste un audit digital gratuit pentru pensiunea sau unitatea ta de cazare. Analizam prezenta online folosind doar informatii publice. Rezultate in 30-90 minute.",
  keywords: [
    "marketing pentru turism",
    "audit digital turism",
    "audit digital gratuit",
    "marketing pensiuni",
    "promovare turistica",
    "audit online cazare",
    "marketing digital turism Romania",
  ],
  authors: [{ name: "DeviDevs Agency", url: "https://devidevs-agency.com" }],
  creator: "DeviDevs Agency",
  publisher: "DeviDevs Agency",
  openGraph: {
    type: "website",
    locale: "ro_RO",
    siteName: "Audit Digital Turism",
    title: "Audit Digital Gratuit pentru Turism | DeviDevs Agency",
    description:
      "Primeste un audit digital gratuit pentru pensiunea sau unitatea ta de cazare. Analizam prezenta online folosind doar informatii publice.",
    url: siteUrl,
    images: [
      {
        url: "/preview-image.png",
        width: 1200,
        height: 630,
        alt: "Audit Digital Turism — DeviDevs Agency",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Audit Digital Gratuit pentru Turism",
    description:
      "Primeste un audit digital gratuit pentru pensiunea ta. Rezultate in 30-90 minute.",
    images: ["/preview-image.png"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};

function JsonLd({ nonce }: { nonce: string }) {
  const organizationSchema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "DeviDevs Agency",
    url: "https://devidevs-agency.com",
    logo: `${siteUrl}/android-chrome-512x512.png`,
  };

  const serviceSchema = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    name: "Audit Digital Turism",
    description:
      "Audit digital gratuit pentru unitati de cazare din Romania. Analiza automata cu AI folosind informatii publice.",
    url: siteUrl,
    provider: {
      "@type": "Organization",
      name: "DeviDevs Agency",
      url: "https://devidevs-agency.com",
    },
    areaServed: {
      "@type": "Country",
      name: "Romania",
    },
    serviceType: "Digital Marketing Audit",
    offers: {
      "@type": "Offer",
      price: "0",
      priceCurrency: "RON",
      description: "Audit digital gratuit",
    },
  };

  return (
    <>
      <script
        nonce={nonce}
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(organizationSchema),
        }}
      />
      <script
        nonce={nonce}
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(serviceSchema),
        }}
      />
    </>
  );
}

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const headersList = await headers();
  const nonce = headersList.get("x-nonce") ?? "";
  const gaId = process.env.NEXT_PUBLIC_GA_ID;

  return (
    <html lang="ro">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <JsonLd nonce={nonce} />
        {gaId && (
          <>
            <Script
              nonce={nonce}
              src={`https://www.googletagmanager.com/gtag/js?id=${gaId}`}
              strategy="afterInteractive"
            />
            <Script nonce={nonce} id="ga4-init" strategy="afterInteractive">
              {`
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());
                gtag('consent', 'default', {
                  'analytics_storage': 'denied',
                  'ad_storage': 'denied',
                  'ad_user_data': 'denied',
                  'ad_personalization': 'denied'
                });
                gtag('config', '${gaId}');
              `}
            </Script>
          </>
        )}
      </head>
      <body
        className={`${inter.variable} ${plusJakartaSans.variable} antialiased`}
      >
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:rounded-lg focus:bg-primary focus:px-4 focus:py-2 focus:text-primary-foreground"
        >
          Salt la conținut
        </a>
        <PageHeader />
        <main id="main-content">{children}</main>
        <PageFooter />
        <Toaster
          theme="light"
          position="bottom-center"
          toastOptions={{
            className: "font-body",
          }}
        />
      </body>
    </html>
  );
}
