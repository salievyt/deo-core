import { articles } from "@/lib/content";
import { notFound } from "next/navigation";
import { PageShell } from "@/components/PageShell";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import type { Metadata } from "next";
export function generateStaticParams() {
  return articles.map((a) => ({ slug: a.slug }));
}
export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const a = articles.find((a) => a.slug === slug);
  return { title: a?.title || "Журнал", description: a?.body[0] };
}
export default async function ArticlePage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const a = articles.find((a) => a.slug === slug);
  if (!a) notFound();
  return (
    <PageShell>
      <article className="article-page">
        <span className="section-label">
          DEO CORE JOURNAL / {a.category.toUpperCase()}
        </span>
        <h1>{a.title}</h1>
        <div className="article-lead">
          Редакция DEO CORE · Октябрь 2026 · {a.time}
        </div>
        <div className="article-body">
          {a.body.map((p, i) => (
            <p key={i}>{p}</p>
          ))}
        </div>
        <Link className="text-link" href="/#insights">
          Все заметки
          <ArrowUpRight size={16} />
        </Link>
      </article>
    </PageShell>
  );
}
