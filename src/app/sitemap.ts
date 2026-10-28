import type { MetadataRoute } from "next";
import { projects, articles } from "@/lib/content";
export const dynamic = "force-static";
export default function sitemap(): MetadataRoute.Sitemap {
  const base = "https://www.deo-core.codes";
  return [
    { url: base + "/", changeFrequency: "monthly", priority: 1 },
    ...projects.map((p) => ({
      url: base + "/projects/" + p.slug + "/",
      priority: 0.8,
    })),
    ...articles.map((a) => ({
      url: base + "/insights/" + a.slug + "/",
      priority: 0.6,
    })),
    { url: base + "/privacy/", priority: 0.2 },
    { url: base + "/terms/", priority: 0.2 },
  ];
}
