from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from index.forms import * # type: ignore
from .models import * # type: ignore
from django.contrib.auth import login, logout # type: ignore
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.views.generic import ListView


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
    product = get_object_or_404(Product, id=id)
    favorite_items = Favorite.objects.filter(user=req.user, product=product)
    is_admin = req.user.is_authenticated and req.user.groups.filter(name='администраторы').exists()
    comments = Comment.objects.filter(product_id=product.id).order_by('-created_at')
    form = CommentForm() if req.user.is_authenticated else None
    extra_content = True if is_admin else ""
    cart_len = len(Cart.objects.filter(user=req.user))
    cart_item = Cart.objects.filter(user=req.user, product=product)
    
    if req.method == 'POST' and req.user.is_authenticated:
        form = CommentForm(req.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = req.user
            comment.product = product
            comment.save()
            form = CommentForm()

    print(comments)
    return render(req, 'product_detail.html', {'product': product,
                                               'form': form,
                                               'comments': comments,
                                               'extra_content': extra_content,
                                               'favorite_items': favorite_items,
                                               'cart_len': cart_len,
                                               'cart_item': cart_item
                                               })

class ProductListView(ListView):
    model = Product
    paginate_by = 3
    template_name = "index.html"
    context_object_name = "data"  # В шаблоне данные будут доступны как {{ data }}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Получаем базовый контекст

        if self.request.user.is_authenticated:
            context["carts_product"] = Cart.objects.filter(user=self.request.user)  # Добавляем корзину в контекст
            context["favorite_product"] = Favorite.objects.filter(user=self.request.user)
            context["total_carts_product"] = len(context["carts_product"])
        else:
            context["carts_product"] = None
            context["favorite_product"] = None
        return context

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
    cart_items = Cart.objects.filter(user=req.user)  # Добавляем корзину в контекст
    favorite_items = Favorite.objects.filter(user=req.user)
    cart_len = len(cart_items)
    print(req)

    total_price = sum(item.total_price() for item in cart_items)
    return render(req, 'profile.html', {'cart_items': cart_items, 
                                        'total_price': total_price,
                                        'favorite_items': favorite_items,
                                        'cart_len': cart_len,
                                        })

@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    favotite_product, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        favotite_product.delete()
    return redirect(f"{request.META.get('HTTP_REFERER', '/')}")

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect(f"{request.META.get('HTTP_REFERER', '/') }")

@login_required
def cart_detail(req):
    favorite_product = Favorite.objects.filter(user=req.user)
    cart_items = Cart.objects.filter(user=req.user) if req.user.is_authenticated else None
    total_price = sum(item.total_price() for item in cart_items)
    cart_len = len(cart_items)

    return render(req, 'cart.html', {'cart_items': cart_items, 
                                     'total_price': total_price,
                                     'cart_len': cart_len,
                                     'favorite_product': favorite_product
                                     })

@login_required
def remove_from_cart(request, cart_id,):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect(f"{request.META.get('HTTP_REFERER', '/')}")

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'shop/favorite_list.html', {'favorites': favorites})