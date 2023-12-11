from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def index(recuest):
    return render(recuest,'index.html')

def author(recuest):
    return render(recuest,'author.html')

@csrf_exempt
def login(recuest):
    if recuest.method == 'POST':
        return HttpResponse('Регистрация прошла успешно')
    return render(recuest,'login.html')

