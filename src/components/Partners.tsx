"use client";
import { useState } from "react";
import { Pause, Play } from "lucide-react";
import { partners as defaultPartners, type Partner } from "@/lib/partners";
import type { Locale } from "@/lib/content";

function PartnerCard({
  partner,
  index,
  ru,
  repeated,
}: {
  partner: Partner;
  index: number;
  ru: boolean;
  repeated: boolean;
}) {
  return (
    <li className="partner-card" aria-hidden={repeated || undefined}>
      {partner.logo ? (
        // Native images keep this static frontend compatible with arbitrary local SVG/PNG logos.
        <img
          src={partner.logo}
          alt={partner.name}
          width={120}
          height={80}
          loading="lazy"
        />
      ) : (
        <div
          className={`partner-placeholder partner-placeholder-${index % 3}`}
          aria-label={
            ru
              ? `Место для логотипа: ${partner.name}`
              : `Partner logo placeholder ${index + 1}`
          }
        >
          <span className="partner-placeholder-number">
            {String(index + 1).padStart(2, "0")}
          </span>
          <span className="partner-placeholder-word">
            LOGO<span>↗</span>
          </span>
          <span className="partner-placeholder-caption">
            {ru ? "ВАШ ЛОГОТИП" : "YOUR LOGO HERE"}
          </span>
        </div>
      )}
    </li>
  );
}

export function Partners({
  lang,
  partners = defaultPartners,
}: {
  lang: Locale;
  partners?: Partner[];
}) {
  const [paused, setPaused] = useState(false);
  const ru = lang === "ru";
  const repetitions = Math.max(4, Math.ceil(24 / Math.max(partners.length, 1)));
  if (!partners.length) return null;
  const row = (reverse: boolean) => {
    const ordered = reverse
      ? [...partners.slice(3), ...partners.slice(0, 3)]
      : partners;
    return (
      <div
        className={`partners-row ${reverse ? "partners-row-reverse" : ""}`}
        aria-hidden={reverse || undefined}
      >
        <div className="partners-track">
          {[0, 1].map((copy) => (
            <ul
              className="partners-group"
              key={copy}
              aria-hidden={copy === 1 || undefined}
            >
              {Array.from(
                { length: repetitions },
                (_, repeat) => repeat,
              ).flatMap((repeat) =>
                ordered.map((partner) => (
                  <PartnerCard
                    key={`${repeat}-${partner.id}`}
                    partner={partner}
                    index={partners.indexOf(partner)}
                    ru={ru}
                    repeated={repeat > 0}
                  />
                )),
              )}
            </ul>
          ))}
        </div>
      </div>
    );
  };
  return (
    <section
      className="partners-section"
      id="partners"
      aria-labelledby="partners-title"
      data-paused={paused}
    >
      <div className="container partners-heading">
        <span className="partners-eyebrow">
          <i />
          CONNECTED BY TRUST
        </span>
        <h2 id="partners-title">{ru ? "Наши партнёры" : "Our partners"}</h2>
        <p>
          {ru
            ? "Компании, с которыми создаём больше."
            : "The companies we build more with."}
        </p>
      </div>
      <div className="partners-rails">
        {row(false)}
        {row(true)}
      </div>
      <div className="container partners-bottom">
        <span>
          {partners.some((partner) => !partner.logo)
            ? ru
              ? "Здесь появятся логотипы наших партнёров."
              : "Our partners’ logos will appear here."
            : ru
              ? "Общие ценности. Сильные партнёрства."
              : "Shared values. Strong partnerships."}
        </span>
        <button
          type="button"
          className="partners-motion-toggle"
          onClick={() => setPaused(!paused)}
          aria-pressed={paused}
          aria-label={
            paused
              ? ru
                ? "Продолжить движение логотипов"
                : "Resume logo animation"
              : ru
                ? "Остановить движение логотипов"
                : "Pause logo animation"
          }
        >
          {paused ? <Play size={12} /> : <Pause size={12} />}
          {paused ? (ru ? "Продолжить" : "Resume") : ru ? "Пауза" : "Pause"}
        </button>
      </div>
    </section>
  );
}
