from pathlib import Path
import re
from zipfile import BadZipFile, ZipFile

from defusedxml import ElementTree
from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError

MAX_FILE_BYTES = 5 * 1024 * 1024


def validate_size(upload):
    if upload.size > MAX_FILE_BYTES:
        raise ValidationError("Файл должен быть не больше 5 MB.")
    if upload.size == 0:
        raise ValidationError("Файл пуст.")


def validate_attachment(upload):
    validate_size(upload)
    extension = Path(upload.name).suffix.lower()
    upload.seek(0)
    try:
        header = upload.read(1024)
        upload.seek(0)
        if extension == ".pdf":
            if not header.startswith(b"%PDF-"):
                raise ValidationError("Содержимое файла не соответствует PDF.")
        elif extension == ".docx":
            try:
                with ZipFile(upload) as archive:
                    names = archive.namelist()
                    if (
                        "[Content_Types].xml" not in names
                        or "word/document.xml" not in names
                    ):
                        raise ValidationError("Некорректный DOCX-файл.")
                    if any(n.lower().endswith("vbaproject.bin") for n in names):
                        raise ValidationError(
                            "Документы с макросами не поддерживаются."
                        )
            except BadZipFile as exc:
                raise ValidationError("Некорректный DOCX-файл.") from exc
        elif extension == ".txt":
            try:
                upload.read().decode("utf-8-sig")
            except UnicodeDecodeError as exc:
                raise ValidationError("TXT должен быть в кодировке UTF-8.") from exc
            if b"\x00" in header:
                raise ValidationError("Некорректный текстовый файл.")
        else:
            raise ValidationError("Допустимы PDF, DOCX и TXT.")
    finally:
        upload.seek(0)


def validate_public_image(upload):
    validate_size(upload)
    extension = Path(upload.name).suffix.lower()
    upload.seek(0)
    try:
        if extension == ".svg":
            try:
                root = ElementTree.fromstring(upload.read())
                if root.tag.split("}")[-1] != "svg":
                    raise ValueError("Not an SVG")
                blocked = {
                    "script",
                    "foreignobject",
                    "iframe",
                    "image",
                    "use",
                    "a",
                    "animate",
                    "set",
                    "style",
                }
                for node in root.iter():
                    if node.tag.split("}")[-1].lower() in blocked:
                        raise ValueError("Active SVG content")
                    for key, value in node.attrib.items():
                        key = key.split("}")[-1].lower()
                        if key.startswith("on") or key in {"href", "src"}:
                            raise ValueError("External or active SVG content")
                        if re.search(
                            r'javascript:|data:|https?:|@import|url\(\s*[\'"]?(?!#)',
                            value,
                            re.I,
                        ):
                            raise ValueError("External SVG resource")
            except Exception as exc:
                raise ValidationError(
                    "SVG должен содержать только статичную векторную графику."
                ) from exc
        elif extension in {".png", ".jpg", ".jpeg", ".webp"}:
            try:
                with Image.open(upload) as image:
                    expected = {
                        ".png": "PNG",
                        ".jpg": "JPEG",
                        ".jpeg": "JPEG",
                        ".webp": "WEBP",
                    }
                    if image.format != expected[extension]:
                        raise ValidationError(
                            "Расширение не соответствует изображению."
                        )
                    if image.width * image.height > 40_000_000:
                        raise ValidationError("Разрешение изображения слишком большое.")
                    image.verify()
            except (
                UnidentifiedImageError,
                OSError,
                Image.DecompressionBombError,
            ) as exc:
                raise ValidationError("Некорректное изображение.") from exc
        else:
            raise ValidationError("Допустимы PNG, JPG, WEBP и статичные SVG.")
    finally:
        upload.seek(0)


def validate_string_list(value):
    if (
        not isinstance(value, list)
        or len(value) > 30
        or any(not isinstance(item, str) or len(item) > 250 for item in value)
    ):
        raise ValidationError(
            "Введите JSON-массив: до 30 строк длиной не больше 250 символов."
        )
