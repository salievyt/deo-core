import { Suspense } from "react";
import { ContentQuery } from "@/components/ContentQuery";
export const metadata = { title: "Журнал" };
export default function Insights() {
  return (
    <Suspense fallback={<p className="content-loading">Загружаем статью…</p>}>
      <ContentQuery kind="article" />
    </Suspense>
  );
}
