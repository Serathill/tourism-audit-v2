import type { Metadata, Viewport } from "next";
import { Suspense } from "react";
import { Inter, Plus_Jakarta_Sans } from "next/font/google";
import { headers } from "next/headers";
import Script from "next/script";
import { Toaster } from "sonner";
import { PageHeader } from "@/components/layout/PageHeader";
import { PageFooter } from "@/components/layout/PageFooter";
import { CookieConsentBanner } from "@/components/CookieConsentBanner";
import { GAListener } from "@/components/GAListener";
import { ScrollDepthTracker } from "@/components/ScrollDepthTracker";
import { ExitIntentPopup } from "@/components/ExitIntentPopup";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin", "latin-ext"],
  display: "swap",
  preload: true,
  adjustFontFallback: true,
});

const plusJakartaSans = Plus_Jakarta_Sans({
  variable: "--font-plus-jakarta-sans",
  subsets: ["latin", "latin-ext"],
  display: "swap",
  preload: true,
  adjustFontFallback: true,
});

const siteUrl =
  process.env.NEXT_PUBLIC_SITE_URL || "https://tourism-audit.devidevs.com";

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
  viewportFit: "cover",
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#0D9488" },
  ],
};

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

  alternates: {
    canonical: "/",
    languages: { "ro-RO": "/" },
  },

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
      {
        url: "/og",
        width: 1200,
        height: 630,
        alt: "Audit Digital Turism",
      },
    ],
  },

  twitter: {
    card: "summary_large_image",
    title: "Audit Digital Gratuit pentru Turism",
    description:
      "Primeste un audit digital gratuit pentru pensiunea ta. Rezultate in 30-90 minute.",
    images: ["/preview-image.png"],
    site: "@Devi__Devs",
    creator: "@Devi__Devs",
  },

  icons: {
    icon: [
      { url: "/favicon.svg", type: "image/svg+xml" },
      { url: "/favicon-16x16.png", sizes: "16x16", type: "image/png" },
      { url: "/favicon-32x32.png", sizes: "32x32", type: "image/png" },
      {
        url: "/android-chrome-192x192.png",
        sizes: "192x192",
        type: "image/png",
      },
      {
        url: "/android-chrome-512x512.png",
        sizes: "512x512",
        type: "image/png",
      },
    ],
    apple: [
      { url: "/apple-touch-icon.png", sizes: "180x180", type: "image/png" },
    ],
    shortcut: "/favicon-32x32.png",
  },

  manifest: "/site.webmanifest",

  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "Audit Digital Turism",
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
    contactPoint: {
      "@type": "ContactPoint",
      email: "contact@devidevs-agency.com",
      contactType: "customer service",
      availableLanguage: ["Romanian", "English"],
    },
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

  const webApplicationSchema = {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    name: "Audit Digital Turism",
    url: siteUrl,
    applicationCategory: "BusinessApplication",
    operatingSystem: "Web",
    offers: {
      "@type": "Offer",
      price: "0",
      priceCurrency: "RON",
      description: "Audit digital gratuit pentru proprietati turistice",
    },
  };

  const webSiteSchema = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    url: siteUrl,
    name: "Audit Digital Turism",
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
      <script
        nonce={nonce}
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(webApplicationSchema),
        }}
      />
      <script
        nonce={nonce}
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(webSiteSchema),
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
        <link rel="preconnect" href="https://www.googletagmanager.com" />
        <link rel="preconnect" href="https://www.google.com" />
        <link
          rel="preconnect"
          href="https://www.gstatic.com"
          crossOrigin="anonymous"
        />
        <link rel="dns-prefetch" href="https://fonts.googleapis.com" />
        <link rel="dns-prefetch" href="https://www.googletagmanager.com" />
        <link rel="dns-prefetch" href="https://www.google.com" />
        <JsonLd nonce={nonce} />
        {gaId && (
          <>
            <script
              nonce={nonce}
              dangerouslySetInnerHTML={{
                __html: `
                  window.dataLayer = window.dataLayer || [];
                  function gtag(){dataLayer.push(arguments);}
                  gtag('consent', 'default', {
                    'analytics_storage': 'denied',
                    'ad_storage': 'denied',
                    'ad_user_data': 'denied',
                    'ad_personalization': 'denied'
                  });
                `,
              }}
            />
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
        <Suspense fallback={null}>
          <GAListener />
        </Suspense>
        <ScrollDepthTracker />
        <CookieConsentBanner />
        <ExitIntentPopup />
      </body>
    </html>
  );
}
