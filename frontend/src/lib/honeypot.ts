import { HONEYPOT_FIELD_NAME } from "@/lib/constants";

/**
 * Returns true if the honeypot field was filled (bot detected).
 * A filled honeypot means the submission should be silently rejected.
 */
export function isHoneypotFilled(body: Record<string, unknown>): boolean {
  const value = body[HONEYPOT_FIELD_NAME];
  return typeof value === "string" && value.length > 0;
}
