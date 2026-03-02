import { ImageResponse } from "next/og";
import type { NextRequest } from "next/server";

export const runtime = "edge";

export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl;
  const title = searchParams.get("title") || "Audit Digital Gratuit pentru Turism";

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          background: "linear-gradient(135deg, #F0FDFA 0%, #FFFFFF 50%, #FFFBEB 100%)",
          fontFamily: "Inter, sans-serif",
        }}
      >
        {/* Brand badge */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            marginBottom: "24px",
          }}
        >
          <div
            style={{
              width: "12px",
              height: "12px",
              borderRadius: "50%",
              background: "#0D9488",
            }}
          />
          <span
            style={{
              fontSize: "20px",
              color: "#0D9488",
              fontWeight: 600,
            }}
          >
            DeviDevs Agency
          </span>
        </div>

        {/* Title */}
        <div
          style={{
            fontSize: "48px",
            fontWeight: 800,
            color: "#0F172A",
            textAlign: "center",
            maxWidth: "900px",
            lineHeight: 1.2,
            padding: "0 40px",
          }}
        >
          {title}
        </div>

        {/* Subtitle */}
        <div
          style={{
            fontSize: "22px",
            color: "#64748B",
            marginTop: "16px",
            textAlign: "center",
            maxWidth: "700px",
          }}
        >
          Analiză automată cu AI din surse publice
        </div>

        {/* CTA pill */}
        <div
          style={{
            marginTop: "32px",
            display: "flex",
            alignItems: "center",
            gap: "8px",
            padding: "12px 28px",
            borderRadius: "9999px",
            background: "linear-gradient(135deg, #F59E0B, #FBBF24)",
            color: "#0F172A",
            fontSize: "18px",
            fontWeight: 700,
          }}
        >
          100% Gratuit — Rezultate în 30-90 min
        </div>
      </div>
    ),
    {
      width: 1200,
      height: 630,
    },
  );
}
