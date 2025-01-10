import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Image, Pdf
import base64
import io
from PIL import Image as PILImage


class FileUploadViewTests(APITestCase):
    def test_upload_image(self):
        url = reverse("file-upload")
        image_data = "data:image/jpeg;base64," + base64.b64encode(
            b"test image data"
        ).decode("utf-8")
        data = {"file_data": image_data}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 1)

    def test_upload_pdf(self):
        url = reverse("file-upload")
        valid_pdf_content = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<<\n/Type /Catalog\n/Outlines 2 0 R\n/Pages 3 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Outlines\n/Count 0\n>>\nendobj\n3 0 obj\n<<\n/Type /Pages\n/Count 1\n/Kids [4 0 R]\n>>\nendobj\n4 0 obj\n<<\n/Type /Page\n/Parent 3 0 R\n/MediaBox [0 0 612 792]\n/Contents 5 0 R\n/Resources <<\n/ProcSet [/PDF /Text]\n/Font <<\n/F1 6 0 R\n>>\n>>\n>>\nendobj\n5 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n(Hello, World!) Tj\nET\nendstream\nendobj\n6 0 obj\n<<\n/Type /Font\n/Subtype /Type1\n/BaseFont /Helvetica\n>>\nendobj\nxref\n0 7\n0000000000 65535 f \n0000000010 00000 n \n0000000074 00000 n \n0000000121 00000 n \n0000000178 00000 n \n0000000331 00000 n \n0000000390 00000 n \ntrailer\n<<\n/Size 7\n/Root 1 0 R\n>>\nstartxref\n455\n%%EOF"
        pdf_data = "data:application/pdf;base64," + base64.b64encode(
            valid_pdf_content
        ).decode("utf-8")
        data = {"file_data": pdf_data}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pdf.objects.count(), 1)

    def test_upload_invalid_file(self):
        url = reverse("file-upload")
        data = {"file_data": "invalid data"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ImagesListTests(APITestCase):
    def test_list_images(self):
        Image.objects.create(original_name="test_image.jpg", file="test_image.jpg")
        url = reverse("images-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class PDFListTests(APITestCase):
    def test_list_pdfs(self):
        Pdf.objects.create(original_name="test_pdf.pdf", file="test_pdf.pdf")
        url = reverse("pdf-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class PdfDetailViewTests(APITestCase):
    def test_get_pdf_detail(self):
        valid_pdf_content = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<<\n/Type /Catalog\n/Outlines 2 0 R\n/Pages 3 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Outlines\n/Count 0\n>>\nendobj\n3 0 obj\n<<\n/Type /Pages\n/Count 1\n/Kids [4 0 R]\n>>\nendobj\n4 0 obj\n<<\n/Type /Page\n/Parent 3 0 R\n/MediaBox [0 0 612 792]\n/Contents 5 0 R\n/Resources <<\n/ProcSet [/PDF /Text]\n/Font <<\n/F1 6 0 R\n>>\n>>\n>>\nendobj\n5 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n(Hello, World!) Tj\nET\nendstream\nendobj\n6 0 obj\n<<\n/Type /Font\n/Subtype /Type1\n/BaseFont /Helvetica\n>>\nendobj\nxref\n0 7\n0000000000 65535 f \n0000000010 00000 n \n0000000074 00000 n \n0000000121 00000 n \n0000000178 00000 n \n0000000331 00000 n \n0000000390 00000 n \ntrailer\n<<\n/Size 7\n/Root 1 0 R\n>>\nstartxref\n455\n%%EOF"
        pdf_file = SimpleUploadedFile(
            "test_pdf.pdf", valid_pdf_content, content_type="application/pdf"
        )
        pdf = Pdf.objects.create(original_name="test_pdf.pdf", file=pdf_file)
        url = reverse("pdf-detail", args=[pdf.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["original_name"], pdf.original_name)


class ImageDetailViewTests(APITestCase):
    def test_get_image_detail(self):
        image_file = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )
        image = Image.objects.create(original_name="test_image.jpg", file=image_file)
        url = reverse("image-detail", kwargs={"pk": image.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["original_name"], image.original_name)


class PdfToImageViewTests(APITestCase):
    def test_convert_pdf_to_images(self):
        valid_pdf_content = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<<\n/Type /Catalog\n/Outlines 2 0 R\n/Pages 3 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Outlines\n/Count 0\n>>\nendobj\n3 0 obj\n<<\n/Type /Pages\n/Count 1\n/Kids [4 0 R]\n>>\nendobj\n4 0 obj\n<<\n/Type /Page\n/Parent 3 0 R\n/MediaBox [0 0 612 792]\n/Contents 5 0 R\n/Resources <<\n/ProcSet [/PDF /Text]\n/Font <<\n/F1 6 0 R\n>>\n>>\n>>\nendobj\n5 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n(Hello, World!) Tj\nET\nendstream\nendobj\n6 0 obj\n<<\n/Type /Font\n/Subtype /Type1\n/BaseFont /Helvetica\n>>\nendobj\nxref\n0 7\n0000000000 65535 f \n0000000010 00000 n \n0000000074 00000 n \n0000000121 00000 n \n0000000178 00000 n \n0000000331 00000 n \n0000000390 00000 n \ntrailer\n<<\n/Size 7\n/Root 1 0 R\n>>\nstartxref\n455\n%%EOF"
        pdf_file = SimpleUploadedFile(
            "test_pdf.pdf", valid_pdf_content, content_type="application/pdf"
        )
        pdf = Pdf.objects.create(original_name="test_pdf.pdf", file=pdf_file)
        url = reverse("pdf-to-images")
        data = {"pdf_id": pdf.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("images", response.data)


class ImageRotateViewTests(APITestCase):
    def test_rotate_image(self):
        # Create a temporary image file
        image = PILImage.new("RGB", (100, 100), color="red")
        image_io = io.BytesIO()
        image.save(image_io, format="JPEG")
        image_io.seek(0)

        image_file = SimpleUploadedFile(
            "test_image.jpg", image_io.read(), content_type="image/jpeg"
        )
        image_instance = Image.objects.create(
            original_name="test_image.jpg", file=image_file
        )
        url = reverse("image-rotate")
        data = {"image_id": image_instance.id, "angle": 90}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("rotated_image", response.data)