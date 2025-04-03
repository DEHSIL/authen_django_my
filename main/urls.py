"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from index.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProductListView.as_view(), name="index"),
    path('profile/', prof, name='prof'),
    path('users/', include('index.urls')),
    path('create/', create, name='create'),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path('favorite/<int:product_id>/', add_to_favorites, name='add_to_favorites'),
    path('favorites/', favorite_list, name='favorite_list'),
    path('cart/add/<int:product_id>/', add_to_cart2, name='add_to_cart2'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/remove/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
