from django.contrib.auth.models import User, AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    sex_choices = (
        (0, "Nữ"),(1, "Nam"), (2, "Không xác định"))
    age = models.IntegerField( default=0)
    sex = models.IntegerField(choices=sex_choices, default=2)
    address = models.CharField(max_length=225, default='')
    
    # You can add additional fields here if needed
    pass