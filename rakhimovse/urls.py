"""rakhimovse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from . import views, telegram_bot
from .api.answerorpaybot.views import webhook as answerorpay_webhook
from .api.datradebot.views import webhook as datradebot_webhook

urlpatterns = [
    path(telegram_bot.ANSWERORPAYBOT_TOKEN, answerorpay_webhook),
    path(telegram_bot.DATRADEBOT_TOKEN, datradebot_webhook),
    path('', views.index),
    path('api/', include('rakhimovse.api.urls')),
    path('admin/', admin.site.urls),
]
