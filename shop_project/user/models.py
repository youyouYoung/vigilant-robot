from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class CustomUser(AbstractUser):
    """
    自定义用户模型，继承自 AbstractUser
    """
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_temporary = models.BooleanField(default=False) # 快速购买用户的标志

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Address(models.Model):
    """
    用户地址，目前要求billing地址只能创建一个，shipping地址可以创建多个
    """
    ADDRESS_TYPE_CHOICES = (
        ('billing', 'Billing'),
        ('shipping', 'Shipping'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)  # e.g., Ontario, Manitoba
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='Canada')

    def __str__(self):
        return f'{self.address_type} - {self.address_line_1}, {self.city}, {self.country}'
