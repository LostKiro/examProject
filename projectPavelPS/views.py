import asyncio

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from projectPavelPS.bot import main
from projectPavelPS.models import UserProfile

@csrf_exempt
def index(request):
    if request.method == 'POST':
        print('BOT Started')
        asyncio.run(main())
    return render(request, 'index.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        if 'email' in request.POST and 'avatar' in request.FILES:
            data = UserProfile.objects.all()
            email = request.POST['email']
            avatar = request.FILES['avatar']
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
        else:
            return HttpResponse('Ошибка: Некорректные данные')
    return render(request, 'login.html')

@csrf_exempt
def author(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = UserProfile.objects.filter(email=email, password=password).first()
            if user:
                return HttpResponse('авторизация прошла успешно')
            else:
                return render(request, 'index.html', {'err': 'авторизация не пройдена'})
        else:
            return HttpResponse('Ошибка: Некорректные данные')
    return render(request, 'author.html')

@csrf_exempt
def start_bot(request):
    return render(request, 'index.html')