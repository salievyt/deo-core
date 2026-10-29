import { Suspense } from "react";
import { ContentQuery } from "@/components/ContentQuery";
export const metadata = { title: "Проекты" };
export default function Projects() {
  return (
    <Suspense fallback={<p className="content-loading">Загружаем проект…</p>}>
      <ContentQuery kind="project" />
    </Suspense>
  );
}
