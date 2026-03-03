import { getStoredUTMParams } from "./utm";

export const GA_TRACKING_ID = process.env.NEXT_PUBLIC_GA_ID;

export function pageview(url: string): void {
  if (!GA_TRACKING_ID) return;
  window.gtag("config", GA_TRACKING_ID, { page_path: url });
}

export function event({
  action,
  category,
  label,
  value,
  params,
}: {
  action: string;
  category: string;
  label?: string;
  value?: number;
  params?: Record<string, unknown>;
}): void {
  if (!GA_TRACKING_ID) return;
  const utmParams = getStoredUTMParams();
  window.gtag("event", action, {
    event_category: category,
    event_label: label,
    value,
    ...utmParams,
    ...params,
  });
}

export function trackScrollDepth(depth: 25 | 50 | 75 | 100): void {
  event({
    action: "scroll_depth",
    category: "engagement",
    label: `${depth}%`,
    value: depth,
  });
}

export function trackCTAClick(
  ctaLabel: string,
  ctaLocation: string,
  ctaVariant?: string
): void {
  event({
    action: "cta_click",
    category: "engagement",
    label: ctaLabel,
    params: {
      cta_location: ctaLocation,
      cta_variant: ctaVariant,
    },
  });
}

export function trackFunnelStep(
  funnelName: string,
  stepName: string,
  stepNumber: number
): void {
  event({
    action: "funnel_step",
    category: "funnel",
    label: stepName,
    value: stepNumber,
    params: {
      funnel_name: funnelName,
      step_name: stepName,
      step_number: stepNumber,
    },
  });
}

export function trackAttribution(
  conversionType: string,
  conversionValue?: number
): void {
  event({
    action: "conversion",
    category: "attribution",
    label: conversionType,
    value: conversionValue,
  });
}
