from django.db import models

# Create your models here.


class product(models.Model):
   name = models.CharField(max_length=255)
   image = models.ImageField(upload_to='products')
   price = models.FloatField()
   span_price = models.FloatField()
   category =models.CharField(max_length=255)
   