from django.db import models

# Create your models here.
class Status(models.Model):
    name =  models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)