
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime



class Product(models.Model): 
    image = models.ImageField(blank=False, upload_to='img/')
    name = models.TextField(blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.created_at}'
