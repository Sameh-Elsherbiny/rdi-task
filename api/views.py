from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageSerializer, PdfSerializer, ImageRotateSerializer ,PdfToImagesSerializer
from .models import Image, Pdf
from .utils import image_or_pdf


class FileUploadView(APIView):
    def post(self, request):
        file_type = image_or_pdf(request.data.get("file_data"))
        if file_type == "image":
            serializer = ImageSerializer(data=request.data)
        elif file_type == "pdf":
            serializer = PdfSerializer(data=request.data)
        else:
            return Response(
                {"message": "Invalid file type"}, status=status.HTTP_400_BAD_REQUEST
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImagesList(generics.ListAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all().values("id", "original_name")


class PDFList(generics.ListAPIView):
    serializer_class = PdfSerializer
    queryset = Pdf.objects.all().values("id", "original_name")


class PdfDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = PdfSerializer

    def get_queryset(self):
        return Pdf.objects.filter(id=self.kwargs["pk"])


class ImageDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        return Image.objects.filter(id=self.kwargs["pk"])


class PdfToImageView(APIView):
    serializer_class = PdfToImagesSerializer
    def post(self, request):
        serializer = PdfToImagesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        pdf_instance = Pdf.objects.get(id=request.data.get("pdf_id"))
        saved_images = ImageSerializer(serializer.convert_pdf_to_images(pdf_instance), many=True).data
        return Response(
            {"message": "PDF converted to images", "images": saved_images},
            status=status.HTTP_201_CREATED,
        )


class ImageRotateView(APIView):
    serializer_class = ImageRotateSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        rotated_image_instance = serializer.validated_data["rotated_image"]
        return Response(
            {
                "message": "Image rotated successfully",
                "rotated_image": rotated_image_instance.file.url,
            },
            status=status.HTTP_201_CREATED,
        )
