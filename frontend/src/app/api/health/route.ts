import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json(
    {
      status: "ok",
      timestamp: new Date().toISOString(),
      service: "tourism-audit-v2-frontend",
    },
    { status: 200 }
  );
}
