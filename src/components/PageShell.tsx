import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Brand } from "./Brand";
export function PageShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="container">
      <header className="inner-header">
        <Link href="/" aria-label="DEO CORE — главная">
          <Brand />
        </Link>
        <Link href="/" className="back-link">
          <ArrowLeft size={15} />
          На главную
        </Link>
      </header>
      <main id="main-content">{children}</main>
      <footer className="simple-footer">
        <span>© 2026 DEO CORE. All rights reserved.</span>
        <Link href="/privacy/">Privacy Policy</Link>
      </footer>
    </div>
  );
}
