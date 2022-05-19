from urllib.parse import urlparse
from django.urls import URLPattern, path
from .views import *


urlpatterns = [
    path('book/', book_room, name = "bookroom"),
    path('food/', food_buy, name = "foodbuy"),
    path('cart/', cart, name = "cart"),
    path('payment/', payment, name = "payment"),
    path('products/', product_list, name = "productlist"),
    # path('products/<id>', product_detail),    รับได้ทุกอย่าง 
    path('products/<int:id>', product_detail),
]