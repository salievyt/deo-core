export type Locale = "ru" | "en";
export type Project = {
  cover?: string | null;
  year?: number;
  status?: string;
  isConcept?: boolean;
  ideaEn?: string;
  solutionEn?: string;
  result?: string;
  resultEn?: string;
  slug: string;
  name: string;
  type: string;
  category: string;
  description: string;
  descriptionEn: string;
  visual: "crm" | "mobile" | "exchange" | "education";
  tags: string[];
  idea: string;
  solution: string;
};
export const projects: Project[] = [
  {
    slug: "deo-crm",
    name: "DEO CRM",
    type: "Business management platform",
    category: "CRM",
    description: "Бизнес под контролем. Всё в одном пространстве.",
    descriptionEn: "Your business, connected in one workspace.",
    visual: "crm",
    tags: ["Product design", "Web development", "Internal product"],
    idea: "Единое рабочее пространство для управления клиентами, проектами и задачами команды.",
    solution:
      "В концепции интерфейса объединены обзор показателей, воронка продаж и список текущих проектов. Фокус — на ясной структуре и быстрых повседневных действиях.",
  },
  {
    slug: "dilz",
    name: "DILZ",
    type: "Mobile experience",
    category: "Mobile",
    description: "Меньше действий. Больше возможностей.",
    descriptionEn: "Fewer steps. More possibilities.",
    visual: "mobile",
    tags: ["Mobile", "UI/UX", "Concept"],
    idea: "Мобильный опыт с простым доступом к основным сценариям продукта.",
    solution:
      "Концептуальная мобильная дизайн-система: контрастная типографика, крупные интерактивные элементы и спокойная визуальная иерархия.",
  },
  {
    slug: "my-exchange",
    name: "My Exchange",
    type: "Finance platform",
    category: "Web",
    description: "Сложные данные. Понятные решения.",
    descriptionEn: "Complex data. Clear decisions.",
    visual: "exchange",
    tags: ["Web app", "UI/UX", "Concept"],
    idea: "Понятное представление финансовых данных в веб-интерфейсе.",
    solution:
      "Визуальная концепция собирает обзор рынка, график и конвертер в одном пространстве. Все значения в демонстрации являются иллюстративными.",
  },
  {
    slug: "ok-erudit",
    name: "ОК Эрудит",
    type: "Education platform",
    category: "UI/UX",
    description: "Интерес к знаниям начинается с опыта.",
    descriptionEn: "A better experience for curious minds.",
    visual: "education",
    tags: ["Education", "UI/UX", "Concept"],
    idea: "Доступная цифровая среда для знакомства с образовательными программами.",
    solution:
      "Концепция строится вокруг простого выбора направления, наглядных карточек и последовательного пути к обучению.",
  },
];
export const services = [
  {
    title: "Product design",
    ru: "От исследования до интерфейса, которым хочется пользоваться. Соединяем потребности людей с задачами вашего бизнеса.",
    en: "From research to interfaces people enjoy. Connecting user needs with your business goals.",
    tags: ["Research & strategy", "UX/UI design", "Design systems"],
    icon: "design",
  },
  {
    title: "Web development",
    ru: "Сайты, веб-приложения и платформы. Быстрые, адаптивные и спроектированные с учётом развития продукта.",
    en: "Websites, applications and platforms. Fast, responsive and designed for your next stage.",
    tags: ["React / Next.js", "TypeScript", "Web applications"],
    icon: "web",
  },
  {
    title: "Mobile development",
    ru: "Мобильные продукты для iOS и Android. Продумываем каждый сценарий — от первого запуска до ежедневного использования.",
    en: "Mobile products for iOS and Android. Thoughtful journeys from the first launch to everyday use.",
    tags: ["Flutter", "iOS / Android", "Cross-platform"],
    icon: "mobile",
  },
  {
    title: "CRM & automation",
    ru: "Внутренние системы, которые помогают команде. Объединяем процессы, данные и инструменты в понятный рабочий поток.",
    en: "Internal systems that help your team. Bringing processes, data and tools into a clear workflow.",
    tags: ["Business systems", "Integrations", "Backend & API"],
    icon: "crm",
  },
];
export const processSteps = [
  {
    title: "Погружаемся в задачу",
    en: "Understand the challenge",
    label: "Discovery & research",
    text: "Знакомимся с вашим бизнесом, пользователями и контекстом. Определяем, какую задачу решает продукт и как будем оценивать результат.",
    textEn:
      "We learn about your business, users and context. Together we define the problem and what success looks like.",
    items: [
      "Бизнес-цели и ограничения",
      "Исследование аудитории",
      "План и границы проекта",
    ],
    itemsEn: [
      "Business goals and constraints",
      "Audience research",
      "Project scope and roadmap",
    ],
  },
  {
    title: "Проектируем опыт",
    en: "Design the experience",
    label: "UX & UI design",
    text: "Превращаем исследование в пользовательские сценарии, прототипы и цельную визуальную систему. Проверяем решения до начала разработки.",
    textEn:
      "We turn research into user journeys, prototypes and a coherent visual system. We validate decisions before development.",
    items: [
      "Пользовательские сценарии",
      "Интерактивный прототип",
      "Дизайн-система",
    ],
    itemsEn: ["User journeys", "Interactive prototype", "Design system"],
  },
  {
    title: "Создаём продукт",
    en: "Build the product",
    label: "Development & testing",
    text: "Дизайнеры и разработчики работают вместе. Выпускаем продукт поэтапно, показываем прогресс и проверяем каждый ключевой сценарий.",
    textEn:
      "Designers and developers work together. We deliver in stages, share progress and test every essential journey.",
    items: [
      "Frontend, mobile и backend",
      "Интеграции и API",
      "Функциональное тестирование",
    ],
    itemsEn: [
      "Frontend, mobile and backend",
      "Integrations and APIs",
      "Functional testing",
    ],
  },
  {
    title: "Запускаем и развиваем",
    en: "Launch and evolve",
    label: "Launch & support",
    text: "Готовим инфраструктуру, выпускаем продукт и помогаем команде освоиться. После запуска работаем над улучшениями и новыми возможностями.",
    textEn:
      "We prepare infrastructure, release the product and help your team get started. Then we improve and add new capabilities.",
    items: [
      "Production-запуск",
      "Документация и передача",
      "Поддержка и развитие",
    ],
    itemsEn: [
      "Production launch",
      "Documentation and handover",
      "Support and evolution",
    ],
  },
];
export const articles = [
  {
    slug: "from-idea-to-mvp",
    category: "Product",
    title: "От идеи до MVP: с чего начинается продукт",
    en: "From idea to MVP: where a product begins",
    time: "5 min",
    body: [
      "Сформулируйте задачу пользователя до выбора технологий. Хороший старт — конкретный ответ на вопрос: кому и в какой ситуации поможет продукт?",
      "Определите один основной сценарий. В первой версии важно проверить полезность решения, а не повторить все возможности зрелой платформы.",
      "Соберите прототип и обсудите его с потенциальными пользователями. Наблюдайте за действиями, а не только за реакцией на визуальную часть.",
      "Зафиксируйте критерии успеха и границы MVP. Договорённость о том, что входит в первый релиз, помогает сохранить фокус и управлять сроками.",
    ],
  },
  {
    slug: "design-as-system",
    category: "Design",
    title: "Дизайн-система: порядок, который помогает расти",
    en: "Design systems: clarity that scales",
    time: "4 min",
    body: [
      "Дизайн-система начинается с правил: типографики, цветов, отступов и поведения элементов. Это общий язык дизайнеров и разработчиков.",
      "Начните с повторяющихся сценариев. Кнопки, поля ввода, навигация и состояния ошибок дадут больше пользы, чем каталог редких компонентов.",
      "Документируйте не только внешний вид, но и назначение. Участникам команды важно понимать, когда использовать компонент и какие задачи он решает.",
      "Развивайте систему вместе с продуктом. Регулярный пересмотр помогает сохранять согласованность и не превращать библиотеку в набор устаревших решений.",
    ],
  },
];
