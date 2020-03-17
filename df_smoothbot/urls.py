# smoothbot/df_smoothbot/urls.py
from django.conf.urls import include, url
from django.urls import path
from .views import home, webhook

urlpatterns = [
    path('home/', home, name='home'),
    path('webhook/', webhook, name='webhook'),
]
