from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from index.forms import * # type: ignore
from .models import *
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required



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
    cart_item = Cart.objects.filter(user=req.user) if req.user.is_authenticated else None
    # print(cart_items)
    # for i in cart_items:
    #     print(i.product)
    # carts_product = [i.product for i in cart_items]
    # print(carts_product)
    products = Product.objects.all()
    return render(req, 'index.html', {'data':products,
                                      'carts_product': cart_item,
                                    #   'carts_product': carts_product
                            
                                               })

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


@login_required
def prof(req):
    cart_items = Cart.objects.filter(user=req.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(req, 'profile.html', {'cart_items': cart_items, 'total_price': total_price})
    # return render(req, 'profile.html')

# @login_required
# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'shop/product_list.html', {'products': products})

@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.get_or_create(user=request.user, product=product)
    return redirect('product_list')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def add_to_cart2(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('index')

@login_required
def cart_detail(req):
    cart_items = Cart.objects.filter(user=req.user) if req.user.is_authenticated else None
    total_price = sum(item.total_price() for item in cart_items)
    return render(req, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('index')

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'shop/favorite_list.html', {'favorites': favorites})