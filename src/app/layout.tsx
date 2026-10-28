import type { Metadata, Viewport } from "next";
import "@fontsource-variable/inter";
import "./globals.css";
export const metadata: Metadata = {
  metadataBase: new URL("https://www.deo-core.codes"),
  title: {
    default: "DEO CORE — Digital Product Studio",
    template: "%s — DEO CORE",
  },
  description:
    "Проектируем и разрабатываем мобильные приложения, сайты, CRM и цифровые сервисы. DEO CORE — студия цифровых продуктов из Кыргызстана.",
  openGraph: {
    title: "DEO CORE — Digital Product Studio",
    description:
      "От идеи до цифрового продукта. Дизайн, разработка и продуктовый подход.",
    locale: "ru_RU",
    type: "website",
    siteName: "DEO CORE",
  },
  robots: { index: true, follow: true },
  icons: { icon: "/icon.svg" },
};
export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#ffffff",
};
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ru">
      <body>
        <a className="skip-link" href="#main-content">
          К содержимому
        </a>
        {children}
      </body>
    </html>
  );
}
