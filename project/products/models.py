from django.db import models

 
# 대화가 끝나서 결과 -> 확인
class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.CharField(max_length=2000, null=True, blank=True)  
    name = models.CharField(max_length=2000, null=True, blank=True)  
    price = models.IntegerField(null=True, blank=True)  
    grade = models.FloatField(null=True, blank=True)
    product_url = models.URLField(max_length=200)
    img_url = models.URLField(max_length=200)
    category1 = models.CharField(max_length=2000, null=True, blank=True)  
    category2 = models.CharField(max_length=2000, null=True, blank=True)  
    category3 = models.CharField(max_length=2000, null=True, blank=True)  
    red = models.IntegerField(null=True, blank=True)
    green = models.IntegerField(null=True, blank=True)
    blue = models.IntegerField(null=True, blank=True)  
    text = models.CharField(max_length=2000, null=True, blank=True)  
    embed = models.CharField(max_length=2000, null=True, blank=True)  
