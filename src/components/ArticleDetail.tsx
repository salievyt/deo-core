"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { API_ENABLED, apiRequest, ApiError, type Article } from "@/lib/api";
import { PageShell } from "./PageShell";
export function ArticleDetail({
  slug,
  initial,
}: {
  slug: string;
  initial?: Article;
}) {
  const [article, setArticle] = useState(initial);
  const [error, setError] = useState("");
  const [retry, setRetry] = useState(0);
  useEffect(() => {
    if (!API_ENABLED) return;
    const controller = new AbortController();
    setError("");
    apiRequest<Article>(`/articles/${encodeURIComponent(slug)}/`, {
      signal: controller.signal,
    })
      .then((data) => {
        setArticle(data);
        document.title = `${data.title} — DEO CORE`;
      })
      .catch((error) => {
        if (!controller.signal.aborted) {
          setArticle(undefined);
          setError(
            error instanceof ApiError && error.status === 404
              ? "Статья не найдена или снята с публикации."
              : "Не удалось загрузить статью. Попробуйте ещё раз.",
          );
        }
      });
    return () => controller.abort();
  }, [slug, retry]);
  if (!article)
    return (
      <PageShell>
        <div className="content-loading" role="status">
          <h1>{error || "Загружаем статью…"}</h1>
          {error && (
            <button className="button dark" onClick={() => setRetry(retry + 1)}>
              Повторить ↗
            </button>
          )}
          <Link href="/#insights" className="text-link">
            Все заметки ↗
          </Link>
        </div>
      </PageShell>
    );
  const a = article;
  return (
    <PageShell>
      <article className="article-page">
        <span className="section-label">
          DEO CORE JOURNAL / {a.category.toUpperCase()}
        </span>
        <h1>{a.title}</h1>
        <div className="article-lead">
          {a.author || "Редакция DEO CORE"} ·{" "}
          {a.published_at
            ? new Date(a.published_at + "T12:00:00").toLocaleDateString("ru-RU")
            : "Октябрь 2026"}{" "}
          · {a.time}
        </div>
        {a.cover && (
          <img className="article-cms-cover" src={a.cover} alt={a.title} />
        )}
        <div className="article-body">
          {a.body.map((p, i) => (
            <p key={i}>{p}</p>
          ))}
        </div>
        <Link className="text-link" href="/#insights">
          Все заметки ↗
        </Link>
      </article>
    </PageShell>
  );
}
