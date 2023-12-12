from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from projectPavelPS.models import ModelRegForm


def index(recuest):
    return render(recuest, 'index.html')


@csrf_exempt
def login(request):
    reg = ModelRegForm()
    if request.method == 'POST':
        data = ModelRegForm.objects.all()
        for i in data:
            if request.POST['email'] == i.email:
                return render(request, 'index.html', {"err": f'Email: {i.email} занят другим пользователем'})
        reg.email = request.POST['email']
        reg.password = request.POST['password']
        reg.login = request.POST['login']
        reg.avatar = request.POST['avatar']
        reg.save()
        return HttpResponse(f'Пользователь с Email: {reg.email} успешно зарегистрирован!')
    return render(request, 'login.html')


@csrf_exempt
def author(request):
    if request.method == 'POST':
        data = ModelRegForm.objects.all()
        for i in data:
            if request.POST['email'] == i.email and request.POST['password'] == i.password:
                return HttpResponse('авторизация прошла успешно')
            else:
                return render(request, 'index.html', {'err': 'авторизация не пройдена'})
    return render(request, 'author.html')
