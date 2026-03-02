import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

// Sliding window: 5 requests per 60 seconds per IP
let ratelimit: Ratelimit | null = null;

function getRatelimit(): Ratelimit | null {
  if (ratelimit) return ratelimit;

  const url = process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.UPSTASH_REDIS_REST_TOKEN;

  if (!url || !token) {
    // Rate limiting disabled when Upstash is not configured
    return null;
  }

  ratelimit = new Ratelimit({
    redis: new Redis({ url, token }),
    limiter: Ratelimit.slidingWindow(5, "60 s"),
    analytics: true,
    prefix: "tourism-audit-v2",
  });

  return ratelimit;
}

export async function checkRateLimit(
  identifier: string
): Promise<{ success: boolean; remaining: number }> {
  const limiter = getRatelimit();

  if (!limiter) {
    // Allow all requests when rate limiting is not configured
    return { success: true, remaining: 5 };
  }

  const result = await limiter.limit(identifier);
  return { success: result.success, remaining: result.remaining };
}
