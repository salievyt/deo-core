import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
export default function NotFound() {
  return (
    <main id="main-content" className="not-found">
      <span className="error-number">404</span>
      <h1>Кажется, здесь ещё нет продукта.</h1>
      <p>Но на главной точно есть что посмотреть.</p>
      <Link className="button dark" href="/">
        Вернуться на главную
        <ArrowUpRight size={17} />
      </Link>
    </main>
  );
}
