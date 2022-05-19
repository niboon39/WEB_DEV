from urllib.parse import urlparse
from django.urls import URLPattern, path
from . import views


urlpatterns = [
    path('hello/', views.say_hello),
    path('bye/', views.say_bye)
]