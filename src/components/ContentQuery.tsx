"use client";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { ProjectDetail } from "./ProjectDetail";
import { ArticleDetail } from "./ArticleDetail";
import { projects, articles } from "@/lib/content";
import { PageShell } from "./PageShell";
export function ContentQuery({ kind }: { kind: "project" | "article" }) {
  const slug = useSearchParams().get("slug");
  if (!slug)
    return (
      <PageShell>
        <div className="content-loading">
          <h1>{kind === "project" ? "Проекты DEO CORE" : "Журнал DEO CORE"}</h1>
          <Link
            className="button dark"
            href={kind === "project" ? "/#projects" : "/#insights"}
          >
            Перейти к списку ↗
          </Link>
        </div>
      </PageShell>
    );
  return kind === "project" ? (
    <ProjectDetail
      key={slug}
      slug={slug}
      initial={projects.find((p) => p.slug === slug)}
    />
  ) : (
    <ArticleDetail
      key={slug}
      slug={slug}
      initial={articles.find((a) => a.slug === slug)}
    />
  );
}
