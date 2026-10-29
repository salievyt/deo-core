from uuid import uuid4
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from .storage import attachment_path, image_path, private_storage
from .validators import validate_attachment, validate_public_image, validate_string_list


class PublishedContent(models.Model):
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    is_published = models.BooleanField("Опубликовано", default=False)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        abstract = True
        ordering = ["sort_order", "pk"]


class SiteSettings(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    site_name = models.CharField("Название", max_length=120, default="DEO CORE")
    hero_title_ru = models.TextField(
        "Заголовок RU",
        default="Превращаем идеи\nв цифровые\nпродукты.",
        help_text="Одна строка текста — одна строка заголовка.",
    )
    hero_title_en = models.TextField(
        "Заголовок EN", default="Turning ideas\ninto digital\nproducts."
    )
    hero_description_ru = models.TextField(
        "Описание RU",
        default="Дизайн, разработка и немного смелости. Создаём приложения, сайты и системы, которые двигают бизнес вперёд.",
    )
    hero_description_en = models.TextField(
        "Описание EN",
        default="Design, development and a little courage. We build apps, websites and systems that move businesses forward.",
    )
    email = models.EmailField("Email", blank=True)
    telegram_url = models.URLField("Telegram", blank=True)
    whatsapp_url = models.URLField("WhatsApp", blank=True)
    instagram_url = models.URLField("Instagram", blank=True)
    linkedin_url = models.URLField("LinkedIn", blank=True)
    github_url = models.URLField("GitHub", blank=True)
    address_ru = models.CharField("Адрес RU", max_length=300, blank=True)
    address_en = models.CharField("Адрес EN", max_length=300, blank=True)
    seo_title_ru = models.CharField(
        "SEO title RU", max_length=200, default="DEO CORE — Digital Product Studio"
    )
    seo_title_en = models.CharField(
        "SEO title EN", max_length=200, default="DEO CORE — Digital Product Studio"
    )
    seo_description_ru = models.CharField(
        "SEO description RU", max_length=350, blank=True
    )
    seo_description_en = models.CharField(
        "SEO description EN", max_length=350, blank=True
    )
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.site_name


class Project(PublishedContent):
    class Status(models.TextChoices):
        RELEASED = "released", "Выпущен"
        DEVELOPMENT = "development", "В разработке"
        CONCEPT = "concept", "Концепция"
        INTERNAL = "internal", "Внутренний продукт"
        NDA = "nda", "NDA"

    name = models.CharField("Название", max_length=160)
    slug = models.SlugField("URL", unique=True)
    product_type = models.CharField("Тип продукта", max_length=160)
    category = models.CharField(
        "Категория",
        max_length=30,
        choices=[
            (v, v)
            for v in ["Web", "Mobile", "CRM", "UI/UX", "Internal Systems", "E-commerce"]
        ],
    )
    industry = models.CharField("Индустрия", max_length=80, blank=True)
    description_ru = models.TextField("Краткое описание RU")
    description_en = models.TextField("Краткое описание EN")
    idea_ru = models.TextField("Задача / идея RU")
    idea_en = models.TextField("Задача / идея EN", blank=True)
    solution_ru = models.TextField("Решение RU")
    solution_en = models.TextField("Решение EN", blank=True)
    result_ru = models.TextField("Результат RU", blank=True)
    result_en = models.TextField("Результат EN", blank=True)
    visual = models.CharField(
        "Резервный макет",
        max_length=20,
        default="crm",
        choices=[(v, v) for v in ["crm", "mobile", "exchange", "education"]],
    )
    cover = models.FileField(
        "Обложка", upload_to=image_path, validators=[validate_public_image], blank=True
    )
    tags = models.JSONField(
        "Теги / технологии",
        default=list,
        validators=[validate_string_list],
        help_text='Например: ["Product design", "React"]',
    )
    year = models.PositiveSmallIntegerField(
        "Год",
        default=2026,
        validators=[MinValueValidator(2000), MaxValueValidator(2100)],
    )
    status = models.CharField(
        "Статус", max_length=20, choices=Status.choices, default=Status.CONCEPT
    )
    is_concept = models.BooleanField("Показывать отметку о концепции", default=True)
    seo_title = models.CharField("SEO title", max_length=200, blank=True)
    seo_description = models.CharField("SEO description", max_length=350, blank=True)

    class Meta(PublishedContent.Meta):
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name


class Service(PublishedContent):
    title = models.CharField("Название", max_length=150)
    description_ru = models.TextField("Описание RU")
    description_en = models.TextField("Описание EN")
    tags = models.JSONField(
        "Компетенции", default=list, validators=[validate_string_list]
    )
    icon = models.CharField(
        "Иконка",
        max_length=20,
        default="web",
        choices=[(v, v) for v in ["design", "web", "mobile", "crm"]],
    )

    class Meta(PublishedContent.Meta):
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.title


class ProcessStep(PublishedContent):
    title_ru = models.CharField("Заголовок RU", max_length=160)
    title_en = models.CharField("Заголовок EN", max_length=160)
    label = models.CharField("Краткое название", max_length=100)
    text_ru = models.TextField("Описание RU")
    text_en = models.TextField("Описание EN")
    items_ru = models.JSONField(
        "Результаты этапа RU", default=list, validators=[validate_string_list]
    )
    items_en = models.JSONField(
        "Результаты этапа EN", default=list, validators=[validate_string_list]
    )

    class Meta(PublishedContent.Meta):
        verbose_name = "Этап работы"
        verbose_name_plural = "Этапы работы"

    def __str__(self):
        return self.title_ru


class Partner(PublishedContent):
    name = models.CharField("Название / подпись", max_length=150)
    logo = models.FileField(
        "Логотип",
        upload_to=image_path,
        blank=True,
        validators=[validate_public_image],
        help_text="PNG, JPG, WEBP или статичный SVG, до 5 MB. Без файла выводится место для логотипа.",
    )

    class Meta(PublishedContent.Meta):
        verbose_name = "Партнёр"
        verbose_name_plural = "Партнёры"

    def __str__(self):
        return self.name


class Article(PublishedContent):
    slug = models.SlugField("URL", unique=True)
    title_ru = models.CharField("Заголовок RU", max_length=250)
    title_en = models.CharField("Заголовок EN", max_length=250)
    category = models.CharField("Категория", max_length=60, default="Product")
    body_ru = models.TextField(
        "Текст RU", help_text="Разделяйте абзацы пустой строкой."
    )
    body_en = models.TextField("Текст EN", blank=True)
    author = models.CharField("Автор", max_length=160, default="Редакция DEO CORE")
    reading_minutes = models.PositiveSmallIntegerField(
        "Минут на чтение",
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(120)],
    )
    cover = models.FileField(
        "Обложка", upload_to=image_path, blank=True, validators=[validate_public_image]
    )
    published_at = models.DateField("Дата публикации", null=True, blank=True)
    seo_title = models.CharField("SEO title", max_length=200, blank=True)
    seo_description = models.CharField("SEO description", max_length=350, blank=True)

    class Meta(PublishedContent.Meta):
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title_ru


class TeamMember(PublishedContent):
    name = models.CharField("Имя", max_length=150)
    role_ru = models.CharField("Должность RU", max_length=150)
    role_en = models.CharField("Должность EN", max_length=150)
    bio_ru = models.TextField("О себе RU", blank=True)
    bio_en = models.TextField("О себе EN", blank=True)
    photo = models.FileField(
        "Фото", upload_to=image_path, blank=True, validators=[validate_public_image]
    )
    linkedin_url = models.URLField("LinkedIn", blank=True)
    github_url = models.URLField("GitHub", blank=True)

    class Meta(PublishedContent.Meta):
        verbose_name = "Участник команды"
        verbose_name_plural = "Команда"

    def __str__(self):
        return self.name


class Technology(PublishedContent):
    name = models.CharField("Название", max_length=100)
    category = models.CharField(
        "Направление",
        max_length=80,
        choices=[
            (v, v)
            for v in ["Mobile", "Frontend", "Backend", "Infrastructure", "Design"]
        ],
    )

    class Meta(PublishedContent.Meta):
        verbose_name = "Технология"
        verbose_name_plural = "Технологии"

    def __str__(self):
        return self.name


class Testimonial(PublishedContent):
    name = models.CharField("Имя", max_length=150)
    company = models.CharField("Компания", max_length=150)
    role = models.CharField("Должность", max_length=150, blank=True)
    text_ru = models.TextField("Отзыв RU")
    text_en = models.TextField("Отзыв EN", blank=True)
    photo = models.FileField(
        "Фото / логотип",
        upload_to=image_path,
        blank=True,
        validators=[validate_public_image],
    )
    project = models.ForeignKey(
        Project, verbose_name="Проект", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta(PublishedContent.Meta):
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"{self.name} — {self.company}"


class Job(PublishedContent):
    slug = models.SlugField("URL", unique=True)
    title_ru = models.CharField("Название RU", max_length=200)
    title_en = models.CharField("Название EN", max_length=200)
    work_format = models.CharField("Формат работы", max_length=150, default="Remote")
    description_ru = models.TextField("Описание RU")
    description_en = models.TextField("Описание EN", blank=True)
    requirements_ru = models.TextField("Требования RU", blank=True)
    requirements_en = models.TextField("Требования EN", blank=True)

    class Meta(PublishedContent.Meta):
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.title_ru


class Statistic(PublishedContent):
    label_ru = models.CharField("Подпись RU", max_length=120)
    label_en = models.CharField("Подпись EN", max_length=120)
    value = models.CharField("Значение", max_length=30)

    class Meta(PublishedContent.Meta):
        verbose_name = "Показатель"
        verbose_name_plural = "Статистика"

    def __str__(self):
        return f"{self.label_ru}: {self.value}"


class Lead(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новая"
        CONTACTED = "contacted", "Связались"
        QUALIFIED = "qualified", "Квалифицирована"
        WON = "won", "Успешно"
        CLOSED = "closed", "Закрыта"
        SPAM = "spam", "Спам"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    idempotency_key = models.UUIDField(
        "Ключ повторной отправки", unique=True, null=True, blank=True, editable=False
    )
    name = models.CharField("Имя", max_length=120)
    company = models.CharField("Компания", max_length=160, blank=True)
    email = models.EmailField("Email")
    contact = models.CharField("Телефон / Telegram", max_length=150, blank=True)
    project_type = models.CharField(
        "Тип проекта",
        max_length=30,
        choices=[
            (v, v)
            for v in [
                "Mobile App",
                "Website",
                "Web App",
                "CRM",
                "UI/UX",
                "Automation",
                "Other",
            ]
        ],
    )
    description = models.TextField("Описание")
    budget = models.CharField(
        "Бюджет",
        max_length=30,
        default="estimate",
        choices=[
            (v, label)
            for v, label in [
                ("estimate", "Нужна оценка"),
                ("under-1000", "до $1,000"),
                ("1000-3000", "$1,000–3,000"),
                ("3000-5000", "$3,000–5,000"),
                ("5000-10000", "$5,000–10,000"),
                ("10000-plus", "$10,000+"),
            ]
        ],
    )
    timeline = models.CharField(
        "Срок",
        max_length=30,
        default="flexible",
        choices=[
            ("flexible", "Не определён"),
            ("asap", "Как можно быстрее"),
            ("1-2 months", "1–2 месяца"),
            ("3-6 months", "3–6 месяцев"),
        ],
    )
    locale = models.CharField(
        "Язык",
        max_length=2,
        choices=[("ru", "Русский"), ("en", "English")],
        default="ru",
    )
    source = models.CharField(
        "Источник", max_length=30, default="Website", editable=False
    )
    kind = models.CharField(
        "Вид обращения",
        max_length=20,
        default="project",
        choices=[("project", "Проект"), ("contact", "Контакт")],
    )
    status = models.CharField(
        "Статус", max_length=20, choices=Status.choices, default=Status.NEW
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Ответственный",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"is_staff": True},
    )
    notes = models.TextField("Внутренние заметки", blank=True)
    consent = models.BooleanField("Согласие на обработку данных", default=False)
    consent_version = models.CharField(
        "Версия политики", max_length=30, default="2026-10-28"
    )
    referrer = models.URLField("Referrer", max_length=2000, blank=True)
    utm_source = models.CharField("UTM source", max_length=250, blank=True)
    utm_medium = models.CharField("UTM medium", max_length=250, blank=True)
    utm_campaign = models.CharField("UTM campaign", max_length=250, blank=True)
    utm_term = models.CharField("UTM term", max_length=250, blank=True)
    utm_content = models.CharField("UTM content", max_length=250, blank=True)
    attachment = models.FileField(
        "Вложение",
        upload_to=attachment_path,
        storage=private_storage,
        blank=True,
        validators=[validate_attachment],
    )
    attachment_name = models.CharField("Имя вложения", max_length=255, blank=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.name} — {self.project_type}"


class LeadDelivery(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Ожидает"
        SENT = "sent", "Доставлено"
        FAILED = "failed", "Ошибка"

    lead = models.OneToOneField(Lead, verbose_name="Заявка", on_delete=models.CASCADE)
    status = models.CharField(
        "Статус", max_length=20, choices=Status.choices, default=Status.PENDING
    )
    attempts = models.PositiveIntegerField("Попыток", default=0)
    last_error = models.CharField("Последняя ошибка", max_length=250, blank=True)
    next_attempt_at = models.DateTimeField("Следующая попытка", null=True, blank=True)
    delivered_at = models.DateTimeField("Доставлено", null=True, blank=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Доставка в CRM"
        verbose_name_plural = "Доставка в CRM"

    def __str__(self):
        return f"CRM / {self.lead_id}"
