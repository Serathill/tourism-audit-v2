import { createClient } from "@supabase/supabase-js";

/**
 * Service role Supabase client — bypasses RLS.
 * Use ONLY in API route handlers, never in client components.
 */
export function createServiceClient() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;

  if (!url || !key) {
    throw new Error(
      "NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set"
    );
  }

  return createClient(url, key, {
    db: { schema: "tourism_audit_v2" },
  });
}
