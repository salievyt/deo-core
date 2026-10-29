import {
  projects,
  services,
  processSteps,
  articles,
  type Project,
} from "./content";
import { partners, type Partner } from "./partners";
export const API_BASE = (process.env.NEXT_PUBLIC_API_URL || "")
  .trim()
  .replace(/\/+$/, "");
export const API_ENABLED = Boolean(API_BASE);
export type Article = (typeof articles)[number] & {
  bodyEn?: string[];
  cover?: string | null;
  author?: string;
  published_at?: string | null;
};
export type SiteSettings = {
  site_name: string;
  hero_title_ru: string;
  hero_title_en: string;
  hero_description_ru: string;
  hero_description_en: string;
  email: string;
  telegram_url: string;
  whatsapp_url: string;
  instagram_url: string;
  linkedin_url: string;
  github_url: string;
  seo_title_ru: string;
  seo_title_en: string;
  seo_description_ru: string;
  seo_description_en: string;
};
export type SiteContent = {
  projects: Project[];
  services: typeof services;
  processSteps: typeof processSteps;
  articles: Article[];
  partners: Partner[];
  technologies: { id?: number; name: string; category: string }[];
  settings: SiteSettings;
};
export const defaultContent: SiteContent = {
  projects,
  services,
  processSteps,
  articles,
  partners,
  technologies: [
    "Next.js",
    "React",
    "Flutter",
    "Python",
    "Django",
    "Figma",
  ].map((name) => ({ name, category: "" })),
  settings: {
    site_name: "DEO CORE",
    hero_title_ru: "Превращаем идеи\nв цифровые\nпродукты.",
    hero_title_en: "Turning ideas\ninto digital\nproducts.",
    hero_description_ru:
      "Дизайн, разработка и немного смелости. Создаём приложения, сайты и системы, которые двигают бизнес вперёд.",
    hero_description_en:
      "Design, development and a little courage. We build apps, websites and systems that move businesses forward.",
    email: "",
    telegram_url: "",
    whatsapp_url: "",
    instagram_url: "",
    linkedin_url: "",
    github_url: "",
    seo_title_ru: "DEO CORE — Digital Product Studio",
    seo_title_en: "DEO CORE — Digital Product Studio",
    seo_description_ru: "",
    seo_description_en: "",
  },
};
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
  }
}
export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    cache: "no-store",
    credentials: "omit",
    signal: options.signal
      ? AbortSignal.any([options.signal, AbortSignal.timeout(20000)])
      : AbortSignal.timeout(20000),
  });
  if (!response.ok) {
    const data = await response.json().catch(() => null);
    const errors =
      data?.errors && typeof data.errors === "object"
        ? Object.values(data.errors)
            .flat()
            .filter((v) => typeof v === "string")
        : [];
    throw new ApiError(
      response.status >= 500
        ? "Сервис временно недоступен. Попробуйте позже."
        : String(errors[0] || data?.message || "Не удалось выполнить запрос."),
      response.status,
    );
  }
  return response.json() as Promise<T>;
}
export function projectHref(slug: string) {
  return API_ENABLED
    ? `/projects/?slug=${encodeURIComponent(slug)}`
    : `/projects/${slug}/`;
}
export function articleHref(slug: string) {
  return API_ENABLED
    ? `/insights/?slug=${encodeURIComponent(slug)}`
    : `/insights/${slug}/`;
}
