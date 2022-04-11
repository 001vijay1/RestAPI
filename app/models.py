from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserAddress(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=200)

    class Meta:
        db_table = 'user_address'

    def __str__(self) -> str:
        return f"{self.user.first_name}-{self.user.last_name}"

class UserVerification(models.Model):
    user = models.CharField(max_length=150)
    otp = models.CharField(max_length=10)

    class Meta:
        db_table = 'user_verification'
    def __str__(self) -> str:
        return self.user