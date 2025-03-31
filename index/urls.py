from django.urls import path, include # type: ignore
# from django.views.generic import TemplateView # type: ignore
from index.views import log, logout_view, reg

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', log, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', reg, name='reg'),
]