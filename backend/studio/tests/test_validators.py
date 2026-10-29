from io import BytesIO
from zipfile import ZipFile
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from studio.validators import validate_public_image, validate_attachment


class FileValidatorTests(SimpleTestCase):
    def test_official_logo_is_allowed_and_active_svg_is_rejected(self):
        validate_public_image(
            SimpleUploadedFile(
                "logo.svg",
                b'<svg xmlns="http://www.w3.org/2000/svg"><path fill="#F08331" d="M0 0h10v10z"/></svg>',
            )
        )
        for body in [
            b"<svg><script>alert(1)</script></svg>",
            b'<svg onload="alert(1)"/>',
            b'<svg><image href="https://example.com/x"/></svg>',
            b'<!DOCTYPE svg [<!ENTITY x SYSTEM "file:///etc/passwd">]><svg>&x;</svg>',
        ]:
            with self.assertRaises(ValidationError):
                validate_public_image(SimpleUploadedFile("bad.svg", body))

    def test_fake_raster_and_invalid_docx_are_rejected(self):
        with self.assertRaises(ValidationError):
            validate_public_image(SimpleUploadedFile("fake.png", b"not an image"))
        with self.assertRaises(ValidationError):
            validate_attachment(SimpleUploadedFile("fake.docx", b"not zip"))
        data = BytesIO()
        with ZipFile(data, "w") as archive:
            archive.writestr("[Content_Types].xml", "<Types/>")
            archive.writestr("word/document.xml", "<document/>")
        validate_attachment(SimpleUploadedFile("valid.docx", data.getvalue()))
