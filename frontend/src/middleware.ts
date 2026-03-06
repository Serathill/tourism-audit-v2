import { type NextRequest, NextResponse } from "next/server";

function buildCspHeader(nonce: string): string {
  const csp = [
    `default-src 'self'`,
    `script-src 'self' 'nonce-${nonce}' 'strict-dynamic' https://www.googletagmanager.com https://www.google.com https://www.gstatic.com`,
    `style-src 'self' 'unsafe-inline' https://fonts.googleapis.com`,
    `font-src 'self' https://fonts.gstatic.com`,
    `img-src 'self' data: blob: https: http:`,
    `connect-src 'self' https://*.supabase.co https://www.google-analytics.com https://region1.google-analytics.com https://www.google.com`,
    `frame-src 'self' https://www.google.com`,
    `frame-ancestors 'none'`,
    `form-action 'self'`,
    `base-uri 'self'`,
    `object-src 'none'`,
  ];
  return csp.join("; ");
}

export async function middleware(request: NextRequest) {
  // Generate crypto nonce for CSP
  const nonce = Buffer.from(crypto.randomUUID()).toString("base64");

  // Pass nonce to layout.tsx via request header
  const requestHeaders = new Headers(request.headers);
  requestHeaders.set("x-nonce", nonce);

  const response = NextResponse.next({
    request: { headers: requestHeaders },
  });

  // Set CSP header (needs per-request nonce — can't live in next.config.ts)
  response.headers.set("Content-Security-Policy", buildCspHeader(nonce));

  // All other security headers live in next.config.ts headers()
  // to avoid duplication and value conflicts.

  return response;
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico)$).*)",
  ],
};
