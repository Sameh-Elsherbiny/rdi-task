from django.db import models
from PyPDF2 import PdfReader


class Image(models.Model):
    file_data= models.TextField()
    file = models.ImageField(upload_to="uploads/")
    original_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name
    
    @property
    def height(self):
        return self.file.height
    
    @property
    def width(self):
        return self.file.width
    
    @property
    def file_location(self):
        return self.file.url
    
class Pdf(models.Model):
    file_data= models.TextField()
    file = models.FileField(upload_to="uploads/")
    original_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name
    
    @property   
    def number_of_pages(self):
        pdf = PdfReader(self.file)
        return len(pdf.pages)
    
    @property
    def page_width(self):
        pdf = PdfReader(self.file)
        return pdf.pages[0].mediabox[2]
    
    @property
    def page_height(self):
        pdf = PdfReader(self.file)
        return pdf.pages[0].mediabox[3]