"use client";
import { useEffect, useState } from "react";
import {
  API_ENABLED,
  apiRequest,
  defaultContent,
  type SiteContent,
} from "./api";
export function useSiteContent() {
  const [content, setContent] = useState<SiteContent>(defaultContent);
  const [contentError, setContentError] = useState(false);
  useEffect(() => {
    if (!API_ENABLED) return;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 12000);
    let active = true;
    apiRequest<SiteContent>("/site/", { signal: controller.signal })
      .then((data) => {
        if (
          !data.settings ||
          ![
            "projects",
            "services",
            "processSteps",
            "articles",
            "partners",
            "technologies",
          ].every((key) => Array.isArray(data[key as keyof SiteContent]))
        )
          throw new Error("Invalid API content");
        if (active) {
          setContent(data);
          setContentError(false);
        }
      })
      .catch(() => {
        if (active) setContentError(true);
      })
      .finally(() => clearTimeout(timeout));
    return () => {
      active = false;
      clearTimeout(timeout);
      controller.abort();
    };
  }, []);
  return { content, contentError };
}
