from urllib.parse import urlparse
from django.urls import URLPattern, path
from .views import register, logout, home_site
from django.contrib.auth.views import LoginView



urlpatterns = [
    path('',LoginView.as_view(), name = "login"),
    path('register/', register, name = "register"),
    path('logout/', logout, name = "logout"),
    path('home/', home_site, name = "home"),
]