import imp
from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, OrderItem
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


def say_hello(request):
    # query_set = Product.objects.filter(inventory__lt=10,unit_price__lt=20)
    # query_set = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    # query_set = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20))
    # query_set = Product.objects.order_by('unit_price','-title').reverse() # เรียงราคาเเละถ้าราคาเท่าจะเรียงตาม title ย้อนกลับ เเละย้อนกลับอีกทีด้วย reverse
    # query_set = Product.objects.all()[5:12]

    # product = Product.objects.order_by('unit_price')[0]
    # product1 = Product.objects.earliest('unit_price')

    # query_set = Product.objects.values('id','title','collection__title') # dictionary
    # query_set = Product.objects.values_list('id','title','collection__title') # dictionary to list

    # query_set = OrderItem.objects.values('product_id').distinct()  #ได้ dictionary ที่บอก id product ที่ order เเต่มีการ order ที่ซ้ำ เเก้โดย distinct
    query_set = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')  # ได้ obkect .tilte เพื่อรู้ชื่อ สุดท้าย sort title
    # query_set = Product.objects.filter(id__in=OrderItem.objects.only('id','title') #ต้องระวังหมายความว่าเลือกเอามาเเค่สองอย่างถ้าหากถามอย่างอื่นรอนานมาก ถ้าไม่อยากได้บางตัวให้ใช้ defer ดีกว่า

    return render(request, 'hello.html', {'name':'Champ','products':list(query_set)})

    # return render(request, 'hello.html', {'name':'Champ','products': product })\
    # return render(request, 'hello.html', {'name':'Champ'})

def say_bye(request):
    return HttpResponse('Good night Champ')


# queryset api >> Field lookups such as gte '>=' lte '<=' range '20,30'