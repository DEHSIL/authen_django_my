from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from index.forms import * # type: ignore
from .models import *
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



def prof(req):
    return render(req, 'profile.html')

def create(req):
    if req.method == 'POST':
        form = ProductForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
            form = ProductForm()
            return redirect('index')  # Перенаправление на список товаров
    else:
        form = ProductForm()

    return render(req, 'create.html', {'form': form})

def product_detail(req, id):
    # is_admin = req.user.is_authenticated and req.user.groups.filter(name='администраторы').exists()
    product = get_object_or_404(Product, id=id)
    comments = Comment.objects.filter(product_id=product.id).order_by('-created_at')
    form = CommentForm() if req.user.is_authenticated else None
    # extra_content = "Административный контент" if is_admin else ""

    if req.method == 'POST' and req.user.is_authenticated:
        form = CommentForm(req.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = req.user
            comment.product = product
            comment.save()
            form = CommentForm()
            # return redirect('product_detail.html')

    print(comments)
    return render(req, 'product_detail.html', {'product': product,
                                               'form': form,
                                               'comments': comments,
                                            #    'extra_content': extra_content
                                               })

def main(req):
    products = Product.objects.all()
    for product in products:
        print(product.id, product.name, product.image.url, product.price, product.description)

    return render(req, 'index.html', {'data':products})

def reg(req):
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(req, 'registration/register.html', {'form': form})

def log(req):
    if req.method == 'POST':
        form = AuthenticationForm(req, data=req.POST)
        if form.is_valid():
            user = form.get_user()
            login(req, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(req, 'registration/login.html', {'form': form})

def logout_view(req):
    logout(req)
    return redirect('index')