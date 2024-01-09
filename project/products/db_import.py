import json
from .models import Products
 
with open('all_data_embed.json', 'r') as file:
    products = json.load(file)
 
for product_data in products:
    Products.objects.create(
        category=product_data.get("category"),
        name=product_data.get("name"),
        price=product_data.get("price"),
        grade=product_data.get("grade"),
        product_url=product_data.get("product_url"),
        img_url=product_data.get("img_url"),
        category1=product_data.get("category1"),
        category2=product_data.get("category2"),
        category3=product_data.get("category3"),
        red=product_data.get("red"),
        green=product_data.get("green"),
        blue=product_data.get("blue"),
        text=product_data.get("text"),
        embed=product_data.get("embed")
    )