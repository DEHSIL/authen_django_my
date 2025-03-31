from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

admin.site.register(Comment)
admin.site.register(Product)

# class CustomUserAdmin(admin.
# ModelAdmin):
#     # list_display = ('username', 'first_name', 'last_name', 'patronymic', 'email', 'is_staff')
#     list_display = ('username',)

# admin.site.register(CustomUser, CustomUserAdmin)