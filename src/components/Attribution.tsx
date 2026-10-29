"use client";
import { useEffect } from "react";
import { API_ENABLED } from "@/lib/api";
import { captureAttribution } from "@/lib/attribution";
export function Attribution() {
  useEffect(() => {
    if (API_ENABLED) captureAttribution();
  }, []);
  return null;
}
