import base64
from django.core.files.base import ContentFile
from io import BytesIO
import uuid
from rest_framework import serializers
from .models import Image, Pdf
from .utils import base64_to_file 
from PIL import Image as PILImage
from pdf2image import convert_from_path
from tempfile import NamedTemporaryFile



class ImageSerializer(serializers.ModelSerializer):
    height = serializers.ReadOnlyField()
    width = serializers.ReadOnlyField()
    file_location = serializers.ReadOnlyField()

    class Meta:
        model = Image
        exclude = ["file"]
        read_only_fields = ["id", "width", "uploaded_at", "original_name"]
        extra_kwargs = {"file_data": {"write_only": True}}

    def create(self, validated_data):
        file_data = validated_data.get("file_data")
        data = base64_to_file(file_data)
        ext = data["ext"]
        validated_data["original_name"] = f"{uuid.uuid4()}.{ext}"
        validated_data["file"] = data["data"]
        return super().create(validated_data)


class PdfSerializer(serializers.ModelSerializer):
    number_of_pages = serializers.ReadOnlyField()
    page_width = serializers.ReadOnlyField()
    page_height = serializers.ReadOnlyField()

    class Meta:
        model = Pdf
        fields = "__all__"
        read_only_fields = ["file", "id", "uploaded_at", "original_name"]
        extra_kwargs = {"file_data": {"write_only": True}}

    def create(self, validated_data):
        file_data = validated_data.get("file_data")
        data = base64_to_file(file_data)
        ext = data["ext"]
        validated_data["file"] = data["data"]
        validated_data["original_name"] = f"{uuid.uuid4()}.{ext}"
        return super().create(validated_data)


class ImageRotateSerializer(serializers.Serializer):
    angel = serializers.IntegerField()
    image_id = serializers.IntegerField()

    def validate(self, data):
        print(data)
        if "angel" in data or "image_id" in data:
            if Image.objects.filter(id=data.get("image_id")).exists():
                image = Image.objects.get(id=data.get("image_id"))

                image.file.open("rb")
                image_io = BytesIO(image.file.read())
                image.file.close()
                image_instance = PILImage.open(image_io)
                rotated_image = image_instance.rotate(data.get("angle", 90))
                rotated_image_io = BytesIO()
                rotated_image.save(rotated_image_io, format="JPEG")
                rotated_image_file = ContentFile(
                    rotated_image_io.getvalue(), name=f"{image.original_name}_rotated.jpg"
                )
                rotated_image_instance = Image(
                    file=rotated_image_file, original_name=f"{image.original_name}_rotated"
                )
                rotated_image_instance.save()
                data["rotated_image"] = rotated_image_instance
            else:
                raise serializers.ValidationError("Image does not exist")
        else:
            raise serializers.ValidationError("angel and image_id are required")
        
        return data
    
class PdfToImagesSerializer(serializers.Serializer):
    pdf_id = serializers.IntegerField()

    def validate(self, data):
        if "pdf_id" in data:
            if  not Pdf.objects.filter(id=data.get("pdf_id")).exists():
                raise serializers.ValidationError("PDF does not exist")
        else:
            raise serializers.ValidationError("pdf_id is required")
        
        return data
    
    def convert_pdf_to_images(self, pdf):
        pdf_file = pdf.file
        pdf_file.open("rb")
        pdf_data = pdf_file.read()
        pdf_file.close()
        with NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
            temp_pdf.write(pdf_data)
            temp_pdf_path = temp_pdf.name
        images = convert_from_path(temp_pdf_path)
        saved_images = []
        for page_num, image in enumerate(images):
            image_io = BytesIO()
            image.save(image_io, format="JPEG")
            image_file = ContentFile(
                image_io.getvalue(), name=f"{pdf.original_name}_page_{page_num}.jpg"
            )
            image_instance = Image(
                file=image_file, original_name=f"{pdf.original_name}_page_{page_num}"
            )
            image_instance.save()
            saved_images.append(image_instance)
        return saved_images
