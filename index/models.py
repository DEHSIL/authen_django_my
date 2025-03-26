from django.contrib.auth.models import AbstractUser
from django.db import models

# class CustomUser(AbstractUser):
#     patronymic = models.CharField(max_length=50, blank=True, null=True, verbose_name='Отчество')

#     def _str_(self):
#         return f"{self.last_name} {self.first_name} {self.patronymic}"

  