from django.db import models

# Create your models here.

class Categorie(models.Model):
    categorie_name = models.CharField(max_length=75, unique=True)
    categorie_url = models.CharField(max_length=150)

    def __str__(self):
        return self.categorie_name

class Product(models.Model):
    product_name = models.CharField(max_length=75, unique=True)
    product_url = models.CharField(max_length=150)
    product_nutriscore = models.CharField(max_length=1)
    product_picture = models.ImageField(upload_to='picture/')
    product_ingredient = models.CharField(max_length=300)
    product_categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
