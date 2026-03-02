import { RECAPTCHA_MIN_SCORE } from "@/lib/constants";

type RecaptchaResult = {
  success: boolean;
  score: number;
  action: string;
};

export async function verifyRecaptcha(
  token: string
): Promise<RecaptchaResult> {
  const secretKey = process.env.RECAPTCHA_SECRET_KEY;

  if (!secretKey) {
    // reCAPTCHA disabled when not configured — allow all
    return { success: true, score: 1.0, action: "submit" };
  }

  const response = await fetch(
    "https://www.google.com/recaptcha/api/siteverify",
    {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        secret: secretKey,
        response: token,
      }),
    }
  );

  const data = await response.json();

  const minScore = Number(process.env.RECAPTCHA_MIN_SCORE) || RECAPTCHA_MIN_SCORE;

  return {
    success: data.success && (data.score ?? 0) >= minScore,
    score: data.score ?? 0,
    action: data.action ?? "",
  };
}
