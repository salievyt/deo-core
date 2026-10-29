"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowUpRight, RotateCcw } from "lucide-react";
import type { Project } from "@/lib/content";
import { API_ENABLED, apiRequest, projectHref, ApiError } from "@/lib/api";
import { PageShell } from "./PageShell";
import { ProjectVisual } from "./ProjectVisual";
export function ProjectDetail({
  slug,
  initial,
  next,
}: {
  slug: string;
  initial?: Project;
  next?: Project;
}) {
  const [project, setProject] = useState<Project | undefined>(initial);
  const [error, setError] = useState("");
  const [retry, setRetry] = useState(0);
  useEffect(() => {
    if (!API_ENABLED) return;
    const controller = new AbortController();
    setError("");
    apiRequest<Project>(`/projects/${encodeURIComponent(slug)}/`, {
      signal: controller.signal,
    })
      .then((data) => {
        setProject(data);
        document.title = `${data.name} — DEO CORE`;
      })
      .catch((error) => {
        if (!controller.signal.aborted) {
          setProject(undefined);
          setError(
            error instanceof ApiError && error.status === 404
              ? "Проект не найден или снят с публикации."
              : "Не удалось загрузить проект. Попробуйте ещё раз.",
          );
        }
      });
    return () => controller.abort();
  }, [slug, retry]);
  if (!project)
    return (
      <PageShell>
        <div className="content-loading" role="status">
          <h1>{error || "Загружаем проект…"}</h1>
          {error && (
            <button className="button dark" onClick={() => setRetry(retry + 1)}>
              Повторить
              <RotateCcw size={16} />
            </button>
          )}
          <Link href="/#projects" className="text-link">
            Все проекты ↗
          </Link>
        </div>
      </PageShell>
    );
  const p = project;
  return (
    <PageShell>
      <section className="case-intro">
        <span className="section-label">
          SELECTED WORK / {p.category.toUpperCase()}
        </span>
        <div className="case-title">
          <h1>{p.name}</h1>
          <p>{p.description}</p>
        </div>
        <div className="case-tags">
          {p.tags.map((tag) => (
            <span key={tag}>{tag}</span>
          ))}
          <span>
            {p.isConcept !== false ? "Visual concept" : p.status || "Project"} ·{" "}
            {p.year || 2026}
          </span>
        </div>
      </section>
      <div className="case-cover">
        <ProjectVisual type={p.visual} cover={p.cover} alt={p.name} />
      </div>
      <div className="case-copy">
        <h2>Идея</h2>
        <p>{p.idea}</p>
      </div>
      <div className="case-copy">
        <h2>Дизайн-подход</h2>
        <p>{p.solution}</p>
      </div>
      {p.result && (
        <div className="case-copy">
          <h2>Результат</h2>
          <p>{p.result}</p>
        </div>
      )}
      {p.isConcept !== false && (
        <p className="case-note">
          Это концептуальная визуализация для демонстрации дизайн-подхода DEO
          CORE. Реальные экраны, состав работ и результаты добавляются после
          подтверждения материалов.
        </p>
      )}
      <div className="case-next">
        <div>
          <span className="eyebrow">
            {next ? "СЛЕДУЮЩИЙ ПРОЕКТ" : "ПОРТФОЛИО"}
          </span>
          <h3>
            <Link href={next ? projectHref(next.slug) : "/#projects"}>
              {next ? next.name : "Все проекты"} ↗
            </Link>
          </h3>
        </div>
        <Link href="/#contact" className="button dark">
          Есть похожая задача?
          <ArrowUpRight size={18} />
        </Link>
      </div>
    </PageShell>
  );
}
