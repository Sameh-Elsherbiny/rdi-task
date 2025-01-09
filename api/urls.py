from django.urls import path
from .views import (
    FileUploadView,
    ImagesList,
    PDFList,
    PdfDetailView,
    ImageDetailView,
    PdfToImageView,
    ImageRotateView,
)

urlpatterns = [
    path("upload/", FileUploadView.as_view(), name="upload_file"),
    path("images/", ImagesList.as_view(), name="list_images"),
    path("pdfs/", PDFList.as_view(), name="list_pdfs"),
    path("pdfs/<int:pk>/", PdfDetailView.as_view(), name="pdf_detail"),
    path("images/<int:pk>/", ImageDetailView.as_view(), name="image_detail"),
    path("convert-pdf-to-image/", PdfToImageView.as_view(), name="pdf_to_image"),
    path("rotate-image/", ImageRotateView.as_view(), name="rotate_image"),
]
