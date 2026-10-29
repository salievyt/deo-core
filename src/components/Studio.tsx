"use client";
import Link from "next/link";
import { useState, useEffect, useRef, type FormEvent } from "react";
import {
  ArrowUpRight,
  ArrowRight,
  ArrowDown,
  Plus,
  Minus,
  Check,
  X,
  Menu,
  Globe,
  Layers3,
  Code2,
  Smartphone,
  Workflow,
  Paperclip,
  CheckCircle2,
} from "lucide-react";
import { Brand, Mark } from "./Brand";
import { ProjectVisual } from "./ProjectVisual";
import { Partners } from "./Partners";
import type { Locale } from "@/lib/content";
import { captureAttribution } from "@/lib/attribution";
import { useSiteContent } from "@/lib/useSiteContent";
import {
  API_ENABLED,
  ApiError,
  apiRequest,
  projectHref,
  articleHref,
} from "@/lib/api";
const icons: Record<string, typeof Code2> = {
  design: Layers3,
  web: Code2,
  mobile: Smartphone,
  crm: Workflow,
};
export function Studio() {
  const { content, contentError } = useSiteContent();
  const {
    projects,
    services,
    processSteps,
    articles,
    partners,
    technologies,
    settings,
  } = content;
  const [lang, setLang] = useState<Locale>("ru");
  const [menu, setMenu] = useState(false);
  const [filter, setFilter] = useState("All");
  const [service, setService] = useState<number | null>(0);
  const [step, setStep] = useState(0);
  const [form, setForm] = useState(false);
  const [faq, setFaq] = useState<number | null>(null);
  const ru = lang === "ru";
  const heroLines = (ru ? settings.hero_title_ru : settings.hero_title_en)
    .split("\n")
    .filter(Boolean);
  const currentStep = processSteps[step] || processSteps[0];
  const t = (a: string, b: string) => (ru ? a : b);
  useEffect(() => {
    document.documentElement.lang = lang;
    return () => {
      document.documentElement.lang = "ru";
    };
  }, [lang]);
  useEffect(() => {
    if (!menu) return;
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = previous;
    };
  }, [menu]);
  const navigation = [
    ["projects", t("Проекты", "Projects")],
    ["services", t("Услуги", "Services")],
    ["studio", t("Студия", "Studio")],
    ["insights", t("Журнал", "Insights")],
  ];
  useEffect(() => {
    setStep((value) => Math.min(value, Math.max(0, processSteps.length - 1)));
  }, [processSteps.length]);
  useEffect(() => {
    document.title = ru ? settings.seo_title_ru : settings.seo_title_en;
    const description = ru
      ? settings.seo_description_ru
      : settings.seo_description_en;
    if (description)
      document
        .querySelector('meta[name="description"]')
        ?.setAttribute("content", description);
  }, [settings, ru]);
  const faqs = ru
    ? [
        [
          "Как начать работу над проектом?",
          API_ENABLED
            ? "Расскажите об идее через форму брифа. Укажите задачу, желаемый срок и ориентировочный бюджет. Заявка поступит команде DEO CORE."
            : "Расскажите об идее через форму брифа. Укажите задачу, желаемый срок и ориентировочный бюджет. Форма поможет подготовить и скачать бриф. Данные остаются в вашем браузере.",
        ],
        [
          "Вы работаете с проектами с нуля?",
          "Да. Помогаем определить задачу, спроектировать пользовательский опыт, разработать MVP и подготовить продукт к запуску. Также можем подключиться на отдельном этапе.",
        ],
        [
          "Сколько стоит разработка?",
          "Стоимость зависит от объёма, интеграций и сложности продукта. Оцениваем работу после знакомства с задачей; фиксируем состав работ, этапы и условия до начала разработки.",
        ],
        [
          "Что происходит после запуска?",
          "Можем продолжить развитие продукта: поддержка, новые функции и улучшение пользовательского опыта. Формат и объём поддержки согласуются отдельно.",
        ],
      ]
    : [
        [
          "How do we get started?",
          API_ENABLED
            ? "Tell us about your idea using the project brief. Include your goals, timeline and approximate budget. Your request will reach the DEO CORE team."
            : "Tell us about your idea using the project brief. Include your goals, timeline and approximate budget. The form helps you prepare and download a brief. Your details stay in your browser.",
        ],
        [
          "Do you build from scratch?",
          "Yes. We help define the problem, design the experience, build an MVP and prepare it for launch. We can also join an existing project at a specific stage.",
        ],
        [
          "How much does development cost?",
          "Cost depends on scope, integrations and complexity. After discovery, we agree on deliverables, stages and terms before development starts.",
        ],
        [
          "What happens after launch?",
          "We can continue with support, new features and user experience improvements. The scope and terms of ongoing support are agreed separately.",
        ],
      ];
  return (
    <>
      <header className="header">
        <div className="container nav">
          <Link href="/" aria-label="DEO CORE — главная">
            <Brand name={settings.site_name} />
          </Link>
          <nav aria-label={t("Основная навигация", "Main navigation")}>
            {navigation.map(([id, label]) => (
              <a key={id} href={"#" + id}>
                {label}
              </a>
            ))}
          </nav>
          <div className="nav-actions">
            <button
              className="language"
              onClick={() => setLang(ru ? "en" : "ru")}
              aria-label={t("Switch to English", "Переключить на русский")}
            >
              {ru ? "RU" : "EN"} <span>⌄</span>
            </button>
            <button className="button small dark" onClick={() => setForm(true)}>
              {t("Обсудить проект", "Start a project")}
              <ArrowUpRight size={16} />
            </button>
            <button
              className="menu-button"
              aria-expanded={menu}
              aria-label={
                menu
                  ? t("Закрыть меню", "Close menu")
                  : t("Открыть меню", "Open menu")
              }
              onClick={() => setMenu(!menu)}
            >
              {menu ? <X /> : <Menu />}
            </button>
          </div>
        </div>
      </header>
      {menu && (
        <nav className="mobile-menu">
          {navigation.map(([id, label]) => (
            <a key={id} href={"#" + id} onClick={() => setMenu(false)}>
              {label}
              <ArrowUpRight />
            </a>
          ))}
          <button
            className="button accent"
            onClick={() => {
              setMenu(false);
              setForm(true);
            }}
          >
            {t("Обсудить проект", "Start a project")}
            <ArrowUpRight size={18} />
          </button>
        </nav>
      )}
      <main id="main-content">
        {contentError && (
          <p className="content-status" role="status">
            {t(
              "Не удалось обновить контент. Показана сохранённая версия сайта.",
              "Could not refresh content. Showing the saved version of the site.",
            )}
          </p>
        )}
        <section className="hero container">
          <div className="hero-eyebrow">
            <span className="eyebrow">
              <i />
              DIGITAL PRODUCT STUDIO
            </span>
            <span className="hero-location">
              BISHKEK, KG <span>↗</span> WORKING GLOBALLY
            </span>
          </div>
          <div className="hero-heading">
            <h1>
              {heroLines.map((line, index) => (
                <span
                  key={index}
                  className={
                    index === heroLines.length - 1 ? "hero-last" : undefined
                  }
                >
                  {index > 0 && <br />}
                  {line}
                  {index === heroLines.length - 2 && (
                    <span className="headline-star">
                      <Mark />
                    </span>
                  )}
                </span>
              ))}
            </h1>
            <div className="hero-aside">
              <div className="orbit-mark">
                <Mark />
                <span>FROM IDEA TO IMPACT</span>
              </div>
              <p>
                {ru
                  ? settings.hero_description_ru
                  : settings.hero_description_en}
              </p>
              <button className="button accent" onClick={() => setForm(true)}>
                {t("Давайте создадим что-то", "Let’s build something")}
                <ArrowUpRight size={20} />
              </button>
            </div>
          </div>
          <div className="hero-bottom">
            <span>
              {t(
                "ОТ ПЕРВОГО «А ЧТО ЕСЛИ» — ДО ЗАПУСКА.",
                "FROM THE FIRST “WHAT IF” TO LAUNCH.",
              )}
            </span>
            <a href="#projects">
              {t("Листайте, будет интересно", "Scroll to explore")}
              <ArrowDown size={15} />
            </a>
          </div>
        </section>
        <section className="projects-section container" id="projects">
          <div className="section-top">
            <div className="section-label">
              <span className="tiny-cross">✳</span>
              {t("ИЗБРАННЫЕ ПРОЕКТЫ", "SELECTED WORK")}
              <sup>{String(projects.length).padStart(2, "0")}</sup>
            </div>
            <span className="subtle-note">
              {t(
                "Разные задачи. Один подход — делать хорошо.",
                "Different challenges. The same care.",
              )}
            </span>
          </div>
          <div className="projects-intro">
            <h2>
              {t("Не просто красиво.", "Beyond good looks.")}
              <br />
              <span className="muted">
                {t("Продумано до сути.", "Thought through.")}
              </span>
            </h2>
            <div
              className="filters"
              role="group"
              aria-label={t("Фильтр проектов", "Project filter")}
            >
              {["All", "Web", "Mobile", "CRM", "UI/UX"].map((f) => (
                <button
                  key={f}
                  className={filter === f ? "active" : ""}
                  onClick={() => setFilter(f)}
                  aria-pressed={filter === f}
                >
                  {f === "All" ? t("Все проекты", "All work") : f}
                  {f === "All" && (
                    <sup>{String(projects.length).padStart(2, "0")}</sup>
                  )}
                </button>
              ))}
            </div>
          </div>
          <div className="project-grid">
            {projects
              .filter((p) => filter === "All" || p.category === filter)
              .map((p) => (
                <Link
                  className={"project-card project-" + p.visual}
                  href={projectHref(p.slug)}
                  key={p.slug}
                >
                  <div className="project-image">
                    <ProjectVisual
                      type={p.visual}
                      cover={p.cover}
                      alt={p.name}
                    />
                    <span className="project-open">
                      <ArrowUpRight size={24} />
                    </span>
                    {p.isConcept !== false && (
                      <span className="concept-label">
                        {t("ВИЗУАЛЬНАЯ КОНЦЕПЦИЯ", "VISUAL CONCEPT")}
                      </span>
                    )}
                  </div>
                  <div className="project-meta">
                    <div>
                      <h3>
                        {p.name}
                        <ArrowUpRight size={18} />
                      </h3>
                      <p>{ru ? p.description : p.descriptionEn}</p>
                    </div>
                    <span>{p.type}</span>
                  </div>
                </Link>
              ))}
          </div>
          <div className="projects-foot">
            <p>
              {projects.some((p) => p.isConcept !== false)
                ? t(
                    "Показываем подход к продукту. Интерфейсы с отметкой — концептуальные визуализации.",
                    "A glimpse of our product thinking. Marked interfaces are conceptual visualizations.",
                  )
                : t(
                    "Дизайн и технологии, которые работают вместе.",
                    "Design and technology working together.",
                  )}
            </p>
            <a className="text-link" href="#services">
              {t("Что мы можем для вас", "Explore our capabilities")}
              <ArrowRight size={17} />
            </a>
          </div>
        </section>
        <section className="services-section" id="services">
          <div className="container">
            <div className="section-label">
              <span className="tiny-cross">✳</span>
              {t("НАШИ ВОЗМОЖНОСТИ", "OUR CAPABILITIES")}
              <sup>02</sup>
            </div>
            <div className="services-layout">
              <div className="services-heading">
                <h2>
                  {t("Ваша задача.", "Your challenge.")}
                  <br />
                  {t("Наша", "Our")}
                  <br />
                  <span>{t("экспертиза.", "expertise.")}</span>
                </h2>
                <p>
                  {t(
                    "Подключаемся там, где нужны. Берём на себя весь цикл — или становимся частью вашей команды.",
                    "Joining where you need us. Taking care of the full cycle — or becoming a part of your team.",
                  )}
                </p>
                <button className="button light" onClick={() => setForm(true)}>
                  {t("Обсудить вашу задачу", "Discuss your challenge")}
                  <ArrowUpRight size={18} />
                </button>
              </div>
              <div className="service-list">
                {services.map((s, i) => {
                  const Icon = icons[s.icon] || Code2;
                  return (
                    <div
                      className={
                        "service-row " + (service === i ? "expanded" : "")
                      }
                      key={s.title}
                    >
                      <button
                        className="service-trigger"
                        onClick={() => setService(service === i ? null : i)}
                        aria-expanded={service === i}
                        aria-controls={"service-" + i}
                      >
                        <span className="service-number">0{i + 1}</span>
                        <Icon size={24} strokeWidth={1.3} />
                        <h3>{s.title}</h3>
                        {service === i ? (
                          <Minus size={20} />
                        ) : (
                          <Plus size={20} />
                        )}
                      </button>
                      <div
                        id={"service-" + i}
                        hidden={service !== i}
                        className="service-detail"
                      >
                        <p>{ru ? s.ru : s.en}</p>
                        <div className="service-tags">
                          {s.tags.map((tag) => (
                            <span key={tag}>{tag}</span>
                          ))}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
            <div className="tech-strip">
              <span>
                {t("ИНСТРУМЕНТЫ ПОД ЗАДАЧУ", "TOOLS FOR THE CHALLENGE")}
              </span>
              <div>
                {technologies.map((technology, i) => (
                  <span key={technology.id || technology.name}>
                    {i > 0 && <i>{i % 2 ? "↗" : "✳"}</i>}
                    {technology.name}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </section>
        <section className="studio-section container" id="studio">
          <div className="section-label">
            <span className="tiny-cross">✳</span>
            {t("НЕМНОГО О НАС", "A LITTLE ABOUT US")}
            <sup>03</sup>
          </div>
          <div className="studio-statement">
            <p>
              {t("Мы — DEO CORE.", "We are DEO CORE.")}
              <br />
              {t(
                "Думаем как продуктовая команда.",
                "Thinking like a product team.",
              )}
              <br />
              <span>
                {t("Создаём как ваша собственная.", "Building like your own.")}
              </span>
            </p>
            <div className="studio-description">
              <p>
                {t(
                  "Мы объединяем стратегию, дизайн и технологии, чтобы превращать сложные задачи в понятные цифровые решения. Без лишних слоёв между идеей и результатом.",
                  "We bring strategy, design and technology together to turn complex challenges into clear digital solutions. A direct path from idea to outcome.",
                )}
              </p>
              <p>
                {t(
                  "Базируемся в Кыргызстане. Работаем без границ. Верим в открытый диалог, сильные решения и продукты, за которыми стоят люди.",
                  "Based in Kyrgyzstan. Working without borders. We believe in open conversations, strong decisions and products built by people, for people.",
                )}
              </p>
              <div className="location-badge">
                <Globe size={17} /> Based in Kyrgyzstan. Working globally.
              </div>
            </div>
          </div>
          <div className="values-grid">
            {(ru
              ? [
                  [
                    "01",
                    "Погружаемся, а не просто делаем",
                    "Разбираемся в вашем бизнесе. Сначала правильные вопросы, потом — решения.",
                  ],
                  [
                    "02",
                    "Одна команда. Общая цель.",
                    "Дизайн и разработка работают вместе — с первого разговора до запуска.",
                  ],
                  [
                    "03",
                    "Прозрачно на каждом этапе",
                    "Показываем прогресс, объясняем решения и остаёмся на связи.",
                  ],
                ]
              : [
                  [
                    "01",
                    "Understand before building",
                    "We learn your business. The right questions come before the solutions.",
                  ],
                  [
                    "02",
                    "One team. Shared purpose.",
                    "Design and development work together, from first conversation to launch.",
                  ],
                  [
                    "03",
                    "Clarity at every stage",
                    "We share progress, explain decisions and stay in touch.",
                  ],
                ]
            ).map(([n, h, p]) => (
              <div className="value" key={n}>
                <span>
                  {n}
                  <ArrowUpRight size={16} />
                </span>
                <h3>{h}</h3>
                <p>{p}</p>
              </div>
            ))}
          </div>
        </section>
        <Partners lang={lang} partners={partners} />
        {currentStep && (
          <section className="process-section">
            <div className="container">
              <div className="section-top">
                <div className="section-label">
                  <span className="tiny-cross">✳</span>
                  {t("КАК МЫ РАБОТАЕМ", "HOW WE WORK")}
                  <sup>04</sup>
                </div>
                <span className="subtle-note">
                  {t(
                    "Понятный процесс. Предсказуемый результат.",
                    "A clear process. A considered outcome.",
                  )}
                </span>
              </div>
              <h2>
                {t("От «есть идея»", "From “I have an idea”")}
                <br />
                <span className="muted">
                  {t("до «мы запустились».", "to “we’re live”.")}
                </span>
              </h2>
              <div
                className="process-tabs"
                role="tablist"
                aria-label={t("Этапы работы", "Process stages")}
              >
                {processSteps.map((s, i) => (
                  <button
                    key={s.label}
                    id={"step-tab-" + i}
                    role="tab"
                    aria-selected={step === i}
                    tabIndex={step === i ? 0 : -1}
                    onKeyDown={(event) => {
                      const keys = ["ArrowLeft", "ArrowRight", "Home", "End"];
                      if (!keys.includes(event.key)) return;
                      event.preventDefault();
                      const next =
                        event.key === "Home"
                          ? 0
                          : event.key === "End"
                            ? processSteps.length - 1
                            : (i +
                                (event.key === "ArrowRight" ? 1 : -1) +
                                processSteps.length) %
                              processSteps.length;
                      setStep(next);
                      document.getElementById("step-tab-" + next)?.focus();
                    }}
                    aria-controls={"step-panel-" + i}
                    onClick={() => setStep(i)}
                    className={step === i ? "active" : ""}
                  >
                    <span>0{i + 1}</span>
                    {s.label}
                    <ArrowUpRight size={17} />
                  </button>
                ))}
              </div>
              <div
                className="process-content"
                id={"step-panel-" + step}
                role="tabpanel"
                aria-labelledby={"step-tab-" + step}
              >
                <div className="process-visual">
                  <div className="process-orbit">
                    <div className="process-center">
                      <Mark />
                    </div>
                    {["Idea", "People", "Product", "Impact"].map((v, i) => (
                      <span key={v} className={"orbit-tag orbit-tag-" + i}>
                        {step === i && <i />}
                        {v}
                      </span>
                    ))}
                    <div className="orbit-path" />
                  </div>
                  <small>GOOD QUESTIONS. BETTER PRODUCTS.</small>
                </div>
                <div className="process-text">
                  <span className="eyebrow">
                    0{step + 1} / {currentStep.label}
                  </span>
                  <h3>{ru ? currentStep.title : currentStep.en}</h3>
                  <p>{ru ? currentStep.text : currentStep.textEn}</p>
                  <ul>
                    {(ru ? currentStep.items : currentStep.itemsEn).map((v) => (
                      <li key={v}>
                        <Check size={15} />
                        {v}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </section>
        )}
        <section className="insights-section container" id="insights">
          <div className="section-top">
            <div className="section-label">
              <span className="tiny-cross">✳</span>
              {t("МЫСЛИ И НАБЛЮДЕНИЯ", "THOUGHTS & OBSERVATIONS")}
              <sup>05</sup>
            </div>
            <span className="subtle-note">
              {t("Делимся тем, как мы думаем.", "A look inside our thinking.")}
            </span>
          </div>
          <div className="insights-title">
            <h2>{t("Внутри процесса.", "Behind the process.")}</h2>
            <span>
              DEO CORE JOURNAL <ArrowUpRight size={16} />
            </span>
          </div>
          <div className="articles-grid">
            {articles.map((a, i) => (
              <Link
                className="article-card"
                href={articleHref(a.slug)}
                key={a.slug}
              >
                <div className={"article-art article-art-" + i}>
                  {a.cover ? (
                    <img
                      className="article-card-cover"
                      src={a.cover}
                      alt={ru ? a.title : a.en}
                      loading="lazy"
                    />
                  ) : i === 0 ? (
                    <>
                      <span className="idea-dot">idea.</span>
                      <div className="idea-path" />
                      <span className="mvp-box">
                        MVP
                        <ArrowUpRight size={30} />
                      </span>
                    </>
                  ) : (
                    <div className="design-demo">
                      <div>
                        <span>Aa</span>
                        <span className="design-circle" />
                      </div>
                      <div>
                        <span className="design-pill">Make it clear. ↗</span>
                        <span className="design-swatch" />
                      </div>
                      <div>
                        <span className="design-lines">╱╱╱╱╱╱</span>
                        <Mark />
                      </div>
                    </div>
                  )}
                  <span className="article-read">
                    <ArrowUpRight size={23} />
                  </span>
                </div>
                <div className="article-caption">
                  <span>
                    {a.category} <i>·</i> {a.time}
                  </span>
                  <h3>{ru ? a.title : a.en}</h3>
                  <span className="article-link">
                    {t("Читать заметку", "Read the note")}
                    <ArrowUpRight size={15} />
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </section>
        <section className="faq-section container">
          <div>
            <div className="section-label">
              <span className="tiny-cross">✳</span>FAQ
            </div>
            <h2>
              {t("Хорошие", "Good")}
              <br />
              {t("вопросы.", "questions.")}
            </h2>
          </div>
          <div className="faq-list">
            {faqs.map(([q, a], i) => (
              <div className="faq-item" key={q}>
                <button
                  aria-expanded={faq === i}
                  aria-controls={"faq-" + i}
                  onClick={() => setFaq(faq === i ? null : i)}
                >
                  {q}
                  {faq === i ? <Minus size={18} /> : <Plus size={18} />}
                </button>
                <p id={"faq-" + i} hidden={faq !== i}>
                  {a}
                </p>
              </div>
            ))}
          </div>
        </section>
        <section className="contact-section" id="contact">
          <div className="container">
            <div className="contact-top">
              <span className="eyebrow">
                <i />
                {t("ОТКРЫТЫ К НОВЫМ ИДЕЯМ", "OPEN TO NEW IDEAS")}
              </span>
              <span>BISHKEK → EVERYWHERE</span>
            </div>
            <div className="contact-heading">
              <h2>
                {t("Большие вещи", "Good things")}
                <br />
                {t("начинаются", "start with")}
                <br />
                <span>{t("с разговора.", "a conversation.")}</span>
              </h2>
              <button
                className="contact-circle"
                onClick={() => setForm(true)}
                aria-label={t("Обсудить проект", "Start a project")}
              >
                <ArrowUpRight />
              </button>
            </div>
            <div className="contact-bottom">
              <p>
                {t(
                  "Есть идея, сложная задача или просто «а что если»?",
                  "An idea, a tough challenge or just a “what if”?",
                )}
                <br />
                {t(
                  "Давайте разберёмся вместе.",
                  "Let’s figure it out together.",
                )}
              </p>
              <button className="text-link" onClick={() => setForm(true)}>
                {t("Расскажите о вашем проекте", "Tell us about your project")}
                <ArrowUpRight size={19} />
              </button>
            </div>
          </div>
        </section>
      </main>
      <footer className="footer container">
        {(settings.email ||
          settings.telegram_url ||
          settings.whatsapp_url ||
          settings.instagram_url ||
          settings.linkedin_url ||
          settings.github_url) && (
          <div className="cms-contacts">
            {settings.email && (
              <a href={"mailto:" + settings.email}>{settings.email} ↗</a>
            )}
            {[
              ["Telegram", settings.telegram_url],
              ["WhatsApp", settings.whatsapp_url],
              ["Instagram", settings.instagram_url],
              ["LinkedIn", settings.linkedin_url],
              ["GitHub", settings.github_url],
            ]
              .filter(([, url]) => url)
              .map(([label, url]) => (
                <a
                  key={label}
                  href={url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {label} ↗
                </a>
              ))}
          </div>
        )}
        <div className="footer-top">
          <Link href="/">
            <Brand name={settings.site_name} />
          </Link>
          <span>
            INDEPENDENT MINDS.
            <br />
            CONNECTED BY CRAFT.
          </span>
          <div>
            {navigation.map(([id, l]) => (
              <a key={id} href={"#" + id}>
                {l}
              </a>
            ))}
          </div>
          <button className="text-link" onClick={() => setForm(true)}>
            {t("Начать проект", "Start a project")}
            <ArrowUpRight size={16} />
          </button>
        </div>
        <div className="footer-bottom">
          <span>© 2026 DEO CORE. All rights reserved.</span>
          <div>
            <Link href="/privacy">Privacy Policy</Link>
            <Link href="/terms">Terms</Link>
            <a href="#" aria-label={t("Наверх", "Back to top")}>
              {t("Наверх", "Back to top")} ↑
            </a>
          </div>
        </div>
      </footer>
      {form && <ProjectForm lang={lang} onClose={() => setForm(false)} />}
    </>
  );
}
function ProjectForm({ lang, onClose }: { lang: Locale; onClose: () => void }) {
  const dialog = useRef<HTMLDialogElement>(null);
  const requestId = useRef<string | null>(null);
  const [selected, setSelected] = useState("Web App");
  const [status, setStatus] = useState<
    "idle" | "sending" | "success" | "error"
  >("idle");
  const [error, setError] = useState("");
  const [fileName, setFileName] = useState("");
  const [draft, setDraft] = useState<Record<string, string> | null>(null);
  const ru = lang === "ru";
  const t = (a: string, b: string) => (ru ? a : b);
  useEffect(() => {
    const el = dialog.current;
    el?.showModal();
    const old = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = old;
      el?.close();
    };
  }, []);
  function saveBrief(fields: Record<string, string>) {
    const labels: Record<string, string> = {
      name: t("Имя", "Name"),
      company: t("Компания", "Company"),
      email: "Email",
      contact: t("Контакт", "Contact"),
      description: t("Описание проекта", "Project description"),
      budget: t("Бюджет", "Budget"),
      timeline: t("Срок", "Timeline"),
      projectType: t("Тип проекта", "Project type"),
    };
    const data = [
      "DEO CORE — Project brief",
      "",
      ...Object.entries(fields)
        .filter(([k]) => labels[k])
        .map(([k, v]) => labels[k] + ": " + v),
      fileName
        ? t(
            "Дополнительный файл (приложите отдельно): ",
            "Supporting file (attach separately): ",
          ) + fileName
        : "",
    ].join("\n");
    const url = URL.createObjectURL(
      new Blob([data], { type: "text/plain;charset=utf-8" }),
    );
    const a = document.createElement("a");
    a.href = url;
    a.download = "deo-core-brief.txt";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (status === "sending") return;
    const fd = new FormData(e.currentTarget);
    fd.set("projectType", selected);
    const fields = Object.fromEntries(
      [...fd.entries()].filter(([, v]) => typeof v === "string"),
    ) as Record<string, string>;
    setDraft(fields);
    if (!API_ENABLED) {
      saveBrief(fields);
      setStatus("success");
      return;
    }
    setStatus("sending");
    setError("");
    requestId.current ||= crypto.randomUUID();
    fd.set("request_id", requestId.current);
    fd.set("consent", "true");
    fd.set("locale", lang);
    for (const [key, value] of Object.entries(captureAttribution()))
      fd.set(key, value || "");
    const attachment = fd.get("attachment");
    if (!(attachment instanceof File) || !attachment.name)
      fd.delete("attachment");
    try {
      const receipt = await apiRequest<{ id: string }>("/project-request/", {
        method: "POST",
        body: fd,
      });
      if (!receipt.id)
        throw new Error(
          t(
            "Не удалось подтвердить получение заявки.",
            "Could not confirm your request.",
          ),
        );
      setStatus("success");
    } catch (error) {
      setError(
        error instanceof ApiError
          ? error.message
          : t(
              "Не удалось отправить заявку. Попробуйте ещё раз.",
              "Could not send your request. Please try again.",
            ),
      );
      setStatus("error");
    }
  }

  return (
    <dialog
      className="brief-dialog"
      aria-labelledby="brief-title"
      ref={dialog}
      onCancel={onClose}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="brief-content">
        <button
          className="close-dialog"
          onClick={onClose}
          aria-label={t("Закрыть", "Close")}
        >
          <X />
        </button>
        {status === "success" ? (
          <div className="success-state">
            <CheckCircle2 size={50} />
            <h2 id="brief-title">
              {API_ENABLED
                ? t("Заявка получена.", "Request received.")
                : t("Бриф готов.", "Your brief is ready.")}
            </h2>
            <p>
              {API_ENABLED
                ? t(
                    "Спасибо. Мы получили вашу заявку и свяжемся с вами.",
                    "Thank you. Your request has been received. We will be in touch.",
                  )
                : t(
                    "Файл сохранён на ваше устройство. Данные никуда не отправлялись. Вы можете дополнить бриф и передать его команде удобным способом.",
                    "Your brief has been downloaded. No details were sent anywhere. You can refine it and share it with the team when you are ready.",
                  )}
            </p>
            <button
              className="button dark"
              onClick={() => draft && saveBrief(draft)}
            >
              {API_ENABLED
                ? t("Скачать копию брифа", "Download a copy")
                : t("Скачать ещё раз", "Download again")}
              <ArrowUpRight size={17} />
            </button>
          </div>
        ) : (
          <>
            <span className="eyebrow">LET’S MAKE SOMETHING MATTER.</span>
            <h2 id="brief-title">
              {t("Расскажите об идее.", "Tell us your idea.")}
            </h2>
            <p className="form-intro">
              {t(
                "Можно без технического задания. Начнём с главного.",
                "No specification needed. Let’s start with what matters.",
              )}
            </p>
            <form onSubmit={submit} aria-busy={status === "sending"}>
              <fieldset>
                <legend>
                  {t("Что будем создавать?", "What are we building?")}
                </legend>
                <div className="type-options">
                  {[
                    "Mobile App",
                    "Website",
                    "Web App",
                    "CRM",
                    "UI/UX",
                    "Automation",
                    "Other",
                  ].map((type) => (
                    <button
                      type="button"
                      key={type}
                      className={selected === type ? "selected" : ""}
                      onClick={() => setSelected(type)}
                      aria-pressed={selected === type}
                    >
                      {type}
                    </button>
                  ))}
                </div>
              </fieldset>
              <div className="form-grid">
                <label>
                  {t("Как вас зовут", "Your name")} *
                  <input
                    name="name"
                    required
                    maxLength={120}
                    autoComplete="name"
                    placeholder={t("Имя", "Name")}
                  />
                </label>
                <label>
                  {t("Компания", "Company")}
                  <input
                    name="company"
                    maxLength={160}
                    autoComplete="organization"
                    placeholder={t("Название компании", "Company name")}
                  />
                </label>
                <label>
                  Email *
                  <input
                    type="email"
                    name="email"
                    required
                    maxLength={254}
                    autoComplete="email"
                    placeholder="you@company.com"
                  />
                </label>
                <label>
                  {t("Телефон или Telegram", "Phone or Telegram")}
                  <input
                    name="contact"
                    maxLength={150}
                    placeholder="+996 … / @username"
                  />
                </label>
              </div>
              <label>
                {t("О проекте", "About the project")} *
                <textarea
                  name="description"
                  required
                  minLength={10}
                  maxLength={5000}
                  rows={3}
                  placeholder={t(
                    "Какую задачу хотите решить? Для кого ваш продукт?",
                    "What problem do you want to solve? Who is it for?",
                  )}
                />
              </label>
              <div className="form-grid">
                <label>
                  {t("Бюджет", "Budget")}
                  <select name="budget">
                    <option value="estimate">
                      {t("Нужна оценка", "Help me estimate")}
                    </option>
                    <option value="under-1000">
                      {t("до $1,000", "Under $1,000")}
                    </option>
                    <option value="1000-3000">$1,000–3,000</option>
                    <option value="3000-5000">$3,000–5,000</option>
                    <option value="5000-10000">$5,000–10,000</option>
                    <option value="10000-plus">$10,000+</option>
                  </select>
                </label>
                <label>
                  {t("Желаемый срок", "Timeline")}
                  <select name="timeline">
                    <option value="flexible">
                      {t("Пока не определён", "Not sure yet")}
                    </option>
                    <option value="asap">
                      {t("Как можно быстрее", "As soon as possible")}
                    </option>
                    <option value="1-2 months">
                      {t("1–2 месяца", "1–2 months")}
                    </option>
                    <option value="3-6 months">
                      {t("3–6 месяцев", "3–6 months")}
                    </option>
                  </select>
                </label>
              </div>
              <label className="file-input">
                <Paperclip size={16} />
                {fileName ||
                  t(
                    "Прикрепить ТЗ или презентацию",
                    "Attach a specification or presentation",
                  )}
                <small>PDF, DOCX, TXT · 5 MB</small>
                <input
                  type="file"
                  name="attachment"
                  accept=".pdf,.docx,.txt"
                  onChange={(e) => {
                    const f = e.target.files?.[0];
                    if (f && f.size > 5 * 1024 * 1024) {
                      e.target.value = "";
                      setFileName("");
                      setError(
                        t(
                          "Файл должен быть меньше 5 MB.",
                          "File must be smaller than 5 MB.",
                        ),
                      );
                      setStatus("error");
                    } else {
                      setFileName(f?.name || "");
                      setError("");
                      setStatus("idle");
                    }
                  }}
                />
              </label>
              <div className="honeypot" aria-hidden="true">
                <label>
                  Website
                  <input name="website" tabIndex={-1} autoComplete="off" />
                </label>
              </div>
              <label className="consent">
                <input type="checkbox" name="consent" required />
                <span>
                  {API_ENABLED
                    ? t(
                        "Согласен на обработку данных для ответа на заявку согласно",
                        "I agree to data processing to respond to my request under the",
                      )
                    : t(
                        "Данные используются только для создания файла в браузере.",
                        "Your details are used only to generate a file in your browser.",
                      )}{" "}
                  <Link href="/privacy" target="_blank">
                    Privacy Policy
                  </Link>
                  .
                </span>
              </label>
              {status === "error" && (
                <div className="form-error" role="alert">
                  {error}
                  {API_ENABLED && draft && (
                    <button
                      type="button"
                      className="text-link"
                      onClick={() => saveBrief(draft)}
                    >
                      {t(
                        "Скачать бриф и сохранить данные",
                        "Download your brief to keep your details",
                      )}{" "}
                      ↓
                    </button>
                  )}
                </div>
              )}
              <button
                className="button accent form-submit"
                type="submit"
                disabled={status === "sending"}
              >
                {status === "sending"
                  ? t("Отправляем…", "Sending…")
                  : API_ENABLED
                    ? t("Отправить заявку", "Send request")
                    : t("Скачать бриф", "Download brief")}
                <ArrowUpRight size={19} />
              </button>
              <p className="form-note">
                {API_ENABLED
                  ? t(
                      "Контакты, описание и выбранный файл будут переданы команде DEO CORE для ответа на вашу заявку.",
                      "Your contact details, project description and selected file will be sent to the DEO CORE team to respond to your request.",
                    )
                  : t(
                      "Бриф скачивается в формате TXT. Прикреплённый файл не загружается на сервер — добавьте его отдельно при передаче брифа.",
                      "Your brief downloads as a TXT file. The supporting file is not uploaded — include it separately when sharing your brief.",
                    )}
              </p>
            </form>
          </>
        )}
      </div>
    </dialog>
  );
}
