import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { ArrowUpRight } from "lucide-react";
import { projects } from "@/lib/content";
import { PageShell } from "@/components/PageShell";
import { ProjectVisual } from "@/components/ProjectVisual";
export function generateStaticParams() {
  return projects.map((p) => ({ slug: p.slug }));
}
export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const p = projects.find((p) => p.slug === slug);
  return { title: p?.name || "Проект", description: p?.description };
}
export default async function ProjectPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const p = projects.find((p) => p.slug === slug);
  if (!p) notFound();
  const next = projects[(projects.indexOf(p) + 1) % projects.length];
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
          {p.tags.map((t) => (
            <span key={t}>{t}</span>
          ))}
          <span>Visual concept · 2026</span>
        </div>
      </section>
      <div className="case-cover">
        <ProjectVisual type={p.visual} />
      </div>
      <div className="case-copy">
        <h2>Идея</h2>
        <p>{p.idea}</p>
      </div>
      <div className="case-copy">
        <h2>Дизайн-подход</h2>
        <p>{p.solution}</p>
      </div>
      <div className="case-copy">
        <h2>В центре — человек</h2>
        <p>
          Ясная иерархия, понятная навигация и минимум лишних действий.
          Интерфейс помогает сосредоточиться на задаче, а единая визуальная
          система делает опыт последовательным на каждом экране.
        </p>
      </div>
      <p className="case-note">
        Это концептуальная визуализация для демонстрации дизайн-подхода DEO
        CORE. Название проекта взято из предоставленного списка. Реальные
        экраны, состав работ и результаты будут добавлены после подтверждения
        материалов.
      </p>
      <div className="case-next">
        <div>
          <span className="eyebrow">СЛЕДУЮЩИЙ ПРОЕКТ</span>
          <h3>
            <Link href={"/projects/" + next.slug}>{next.name} ↗</Link>
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
