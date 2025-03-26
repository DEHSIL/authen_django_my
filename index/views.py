from django.shortcuts import render, redirect # type: ignore
from index.forms import * # type: ignore
from django.views import View # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
# from .models import CustomUser # type: ignore


def prof(req):
    return render(req, 'profile.html')

# def reg(req):
#     if req.method == "POST":
#             form = CustomUser(req.POST)
#             print(form)
#             if form.is_valid():
#                 user = form.save()
#                 login(req, user)
#             return redirect('index')
#     else:
#         form = CustomUser()

#         return render(req, 'registration/register.html')

# def log(req):
#     return render(req, 'login.html')
    
# def logout_view(req):
#     logout(req)  # Завершаем сессию пользователя
#     return redirect('index')  # Перенаправляем на главную страницу
