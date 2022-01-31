"""smartgarden URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from smartgardenapp.views import home_view
from smartgardenapp.views import mode_view
from smartgardenapp.views import startwater
from smartgardenapp.views import stopwater
from smartgardenapp.views import autoClick
from smartgardenapp.views import setmanual
from smartgardenapp.views import setlong
from smartgardenapp.views import setlat
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('index.html', home_view, name='home'),
    path('modes.html', mode_view, name="modes"),
    path('stopWater',stopwater),
    path('startWater',startwater),
    path('setManual',setmanual),
    path('setAuto',autoClick),
    path('setLong',setlong),
    path('setLat',setlat)
]
