from django import forms # type: ignore
from .models import Comment, Product

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image', 'name', 'price', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }