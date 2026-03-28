// ═══════════════════════════════════════════════════════════
// Tourism Audit V2 — Constants
// ═══════════════════════════════════════════════════════════

// ── Romanian Counties grouped by Development Region ──────

export type Region = {
  name: string;
  counties: string[];
};

export const REGIONS: Region[] = [
  {
    name: "Nord-Est",
    counties: ["Bacău", "Botoșani", "Iași", "Neamț", "Suceava", "Vaslui"],
  },
  {
    name: "Sud-Est",
    counties: ["Brăila", "Buzău", "Constanța", "Galați", "Tulcea", "Vrancea"],
  },
  {
    name: "Sud-Muntenia",
    counties: [
      "Argeș",
      "Călărași",
      "Dâmbovița",
      "Giurgiu",
      "Ialomița",
      "Prahova",
      "Teleorman",
    ],
  },
  {
    name: "Sud-Vest Oltenia",
    counties: ["Dolj", "Gorj", "Mehedinți", "Olt", "Vâlcea"],
  },
  {
    name: "Vest",
    counties: ["Arad", "Caraș-Severin", "Hunedoara", "Timiș"],
  },
  {
    name: "Nord-Vest",
    counties: [
      "Bihor",
      "Bistrița-Năsăud",
      "Cluj",
      "Maramureș",
      "Satu Mare",
      "Sălaj",
    ],
  },
  {
    name: "Centru",
    counties: ["Alba", "Brașov", "Covasna", "Harghita", "Mureș", "Sibiu"],
  },
  {
    name: "București-Ilfov",
    counties: ["București", "Ilfov"],
  },
];

// Flat list of all counties for validation
export const ALL_COUNTIES = REGIONS.flatMap((r) => r.counties);

// ── Navigation ──────────────────────────────────────────

export type NavLink = {
  label: string;
  href: string;
};

export const NAV_LINKS: NavLink[] = [
  { label: "Marketing", href: "/marketing-pentru-turism" },
  { label: "Servicii", href: "/servicii" },
  { label: "Despre noi", href: "/despre-noi" },
];

export const AUDIT_CTA_LINK: NavLink = {
  label: "Solicită audit",
  href: "/audit",
};

export const LEGAL_LINKS: NavLink[] = [
  { label: "Politica de confidențialitate", href: "/privacy-policy" },
  { label: "Termeni și condiții", href: "/terms-and-conditions" },
];

// ── Team Data ───────────────────────────────────────────

export type TeamMember = {
  name: string;
  role: string;
  description: string;
  image: string;
};

export const TEAM_MEMBERS: TeamMember[] = [
  {
    name: "Petru Constantin",
    role: "CEO & Founder",
    description: "Dezvoltare de business și relații cu clienții",
    image: "/images/team/petru-constantin.webp",
  },
  {
    name: "Nicu Constantin",
    role: "CTO & Co-Founder",
    description: "Tehnologie AI și automatizare de marketing",
    image: "/images/team/nicu-constantin.webp",
  },
  {
    name: "Alexandru Mihailă",
    role: "Developer",
    description:
      "Strategie de marketing digital și consultanță pentru turism",
    image: "/images/team/alexandru-mihaila.jpg",
  },
];

// ── Brand ───────────────────────────────────────────────

export const BRAND = {
  name: "Audit Digital Turism",
  tagline: "Un serviciu de la DeviDevs Agency",
  parentName: "DeviDevs Agency",
  parentUrl: "https://devidevs-agency.com",
  email: "contact@audit-turism.ro",
} as const;

// ── Form ────────────────────────────────────────────────

export const MAX_FORM_STEPS = 3;
export const RECAPTCHA_MIN_SCORE = 0.5;
export const MAX_DESCRIPTION_LENGTH = 1000;
export const HONEYPOT_FIELD_NAME =
  process.env.NEXT_PUBLIC_HONEYPOT_FIELD_NAME ?? "_hp_website";
