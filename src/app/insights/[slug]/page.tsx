import { articles } from "@/lib/content";
import { notFound } from "next/navigation";
import { ArticleDetail } from "@/components/ArticleDetail";
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
  return <ArticleDetail slug={slug} initial={a} />;
}
