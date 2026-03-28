import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

type RateLimitConfig = { limit: number; windowSeconds: number };

/** Pre-defined rate limit profiles per route type. */
export const RATE_LIMITS = {
  /** Audit submission — generation is resource-intensive. */
  auditSubmit: { limit: 3, windowSeconds: 3600 } as RateLimitConfig,
  /** Contact / consultation forms. */
  contactForm: { limit: 5, windowSeconds: 60 } as RateLimitConfig,
  /** GDPR data export / deletion requests. */
  gdprRequest: { limit: 3, windowSeconds: 300 } as RateLimitConfig,
  /** Default fallback. */
  default: { limit: 5, windowSeconds: 60 } as RateLimitConfig,
} as const;

// Reuse Redis connection across limiters
let redis: Redis | null = null;

function getRedis(): Redis | null {
  if (redis) return redis;

  const url = process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.UPSTASH_REDIS_REST_TOKEN;

  if (!url || !token) return null;

  redis = new Redis({ url, token });
  return redis;
}

// Cache limiter instances by config key to avoid re-creation
const limiters = new Map<string, Ratelimit>();

function getLimiter(config: RateLimitConfig): Ratelimit | null {
  const r = getRedis();
  if (!r) return null;

  const key = `${config.limit}:${config.windowSeconds}`;
  if (!limiters.has(key)) {
    limiters.set(
      key,
      new Ratelimit({
        redis: r,
        limiter: Ratelimit.slidingWindow(config.limit, `${config.windowSeconds} s`),
        analytics: true,
        prefix: "tourism-audit-v2",
      })
    );
  }
  return limiters.get(key)!;
}

export async function checkRateLimit(
  identifier: string,
  config: RateLimitConfig = RATE_LIMITS.default
): Promise<{ success: boolean; remaining: number }> {
  const limiter = getLimiter(config);

  if (!limiter) {
    // Allow all requests when Upstash is not configured (dev mode)
    return { success: true, remaining: config.limit };
  }

  const result = await limiter.limit(identifier);
  return { success: result.success, remaining: result.remaining };
}

export function getClientIp(headers: Headers): string {
  return (
    headers.get("x-forwarded-for")?.split(",")[0]?.trim() ??
    headers.get("x-real-ip") ??
    "unknown"
  );
}
