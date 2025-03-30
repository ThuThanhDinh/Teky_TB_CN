from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)  # ID tự tăng
    name = models.CharField(max_length=255)  
    email = models.TextField()  
    password = models.TextField()  
    phone = models.TextField()


    def __str__(self):
       
        return self.name  