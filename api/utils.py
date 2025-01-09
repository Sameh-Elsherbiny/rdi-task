from django.core.files.base import ContentFile
import base64

def image_or_pdf(file_data):
    if file_data.startswith("data:"):
        mime_type = file_data.split(";")[0].split(":")[1]
        if mime_type.startswith("image/"):
            return "image"
        elif mime_type == "application/pdf":
            return "pdf"
        else:
            return "unknown"
        
def base64_to_file(file_data):
    format, imgstr = file_data.split(';base64,')
    ext = format.split('/')[-1]
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    return {"data": data, "ext": ext}