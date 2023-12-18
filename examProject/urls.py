from django.contrib import admin
from django.urls import path
from projectPavelPS import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('author/', views.author),
    path('login/', views.login),
    # path('start-bot/', views.start_bot, name='start_bot')
]
