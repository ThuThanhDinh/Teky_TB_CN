from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product', blank=True, null=True)

    def __str__(self):
        return self.name

class post(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()

    def __str__(self):
        return self.name
    
class employ(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()

    def __str__(self):
        return self.name
class User(models.Model):
    id = models.AutoField(primary_key=True)  # ID tự tăng
    username = models.CharField(max_length=255)  
    email = models.TextField()  
    password = models.TextField()  

    def __str__(self):
        
        return self.name    