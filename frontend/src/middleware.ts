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

  // Set CSP header
  response.headers.set("Content-Security-Policy", buildCspHeader(nonce));

  // Security headers
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("X-XSS-Protection", "1; mode=block");
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  response.headers.set(
    "Permissions-Policy",
    "camera=(), microphone=(), geolocation=()"
  );
  response.headers.set(
    "Strict-Transport-Security",
    "max-age=63072000; includeSubDomains; preload"
  );

  return response;
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico)$).*)",
  ],
};
