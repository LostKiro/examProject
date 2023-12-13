import asyncio

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
# from projectPavelPS.forms import RegistrationForm, UserProfileForm
from projectPavelPS.models import UserProfile


def index(recuest):
    return render(recuest, 'index.html')



@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = UserProfile.objects.all()
        email = request.POST['email']
        avatar = request.FILES['avatar']  # Получаем файл изображения

        for i in data:
            if email == i.email:
                return render(request, 'index.html', {"err": f'Email {email} занят другим пользователем'})

        reg = UserProfile()
        reg.email = email
        reg.password = request.POST['password']
        reg.login = request.POST['login']
        reg.avatar = avatar
        reg.save()

        return HttpResponse(f'Пользователь с Email: {reg.email} успешно зарегистрирован!')

    return render(request, 'login.html')

@csrf_exempt
def author(request):
    if request.method == 'POST':
        data = UserProfile.objects.all()
        for i in data:
            if request.POST['email'] == i.email and request.POST['password'] == i.password:
                return HttpResponse('авторизация прошла успешно')
            else:
                return render(request, 'index.html', {'err': 'авторизация не пройдена'})
    return render(request, 'author.html')

@csrf_exempt
def index(request):
    if request.method == 'POST':
        asyncio.run(main()) #запуск бота
    return render(request, 'index.html')
