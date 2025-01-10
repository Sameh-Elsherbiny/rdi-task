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
    path("upload/", FileUploadView.as_view(), name="file-upload"),
    path("images/", ImagesList.as_view(), name="images-list"),
    path("pdfs/", PDFList.as_view(), name="pdf-list"),
    path("pdfs/<int:pk>/", PdfDetailView.as_view(), name="pdf-detail"),
    path("images/<int:pk>/", ImageDetailView.as_view(), name="image-detail"),
    path("convert-pdf-to-image/", PdfToImageView.as_view(), name="pdf-to-images"),
    path("rotate-image/", ImageRotateView.as_view(), name="image-rotate"),
]
