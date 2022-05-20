from multiprocessing.dummy import current_process
from tabnanny import check
from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import BuyForm, UpdateForm, PaymentForm, BookingForm
from .models import Menu,Cart,Ordercart, Room, Booking
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pypromptpay import qr_code
import datetime
import os
import cv2 as cv
from . import Slippayment as Bp
from PIL import Image
from decimal import *

@login_required
def book_room(request):
    user = request.user
    urlroom = ["/media/topview/normal.jpg"]
    button = ""
    checkin = datetime.datetime.now()
    checkout = datetime.datetime.now()

    if 'room' in request.POST:
        allroom = Room.objects.all()
        numroom = request.POST.get('numroom')
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        epoch_checkin = datetime.datetime(int(checkin[0:4]) ,int( checkin[5:7]) , int(checkin[8:10]) , 0 , 0).timestamp()
        epoch_checkout = datetime.datetime(int(checkout[0:4]) ,int( checkout[5:7]) , int(checkout[8:10]) , 0 , 0).timestamp()
        day = (epoch_checkout - epoch_checkin)/86400
        price = allroom[int(numroom)].unit_price*Decimal(day)
        UserBooking = Booking(user=user,room=allroom[int(numroom)],checkin=checkin,checkout=checkout,day=day,total_price=price)
        UserBooking.save()
        messages.success(request, f'Add room "{allroom[int(numroom)].title}" in cart Successsfully!')
        return redirect('cart')

    if 'search' in request.POST:
        form = BookingForm(request.POST)
        if form.is_valid():
            checkin = request.POST.get('checkin')
            checkout = request.POST.get('checkout')
            people = int(request.POST.get('people'))
            code = ''

            epoch_checkin = datetime.datetime(int(checkin[0:4]) ,int( checkin[5:7]) , int(checkin[8:10]) , 0 , 0).timestamp()
            epoch_checkout = datetime.datetime(int(checkout[0:4]) ,int( checkout[5:7]) , int(checkout[8:10]) , 0 , 0).timestamp()

            allroom = Room.objects.all()
            for room in allroom:
                if int(room.people) < people:
                    code += '0'
                else:
                    epoch_book = [epoch_checkin+1,epoch_checkout]   #user checkinout
                    allbook = Booking.objects.filter(room=room)
                    avaliable = '1'
                    print(room.title)
                    for book in allbook:
                        checkin2 = str(book.checkin)
                        checkout2 = str(book.checkout)
                        epoch_checkin2 = datetime.datetime(int(checkin2[0:4]) ,int(checkin2[5:7]) , int(checkin2[8:10]) , 0 , 0).timestamp()
                        epoch_checkout2 = datetime.datetime(int(checkout2[0:4]) ,int( checkout2[5:7]) , int(checkout2[8:10]) , 0 , 0).timestamp()
                        epoch_booked = [epoch_checkin2,epoch_checkout2]   #booked checkinout

                        f_in , f_out , f_cover = 0 , 0 , 0
                        if epoch_book[0] > epoch_booked[0] and epoch_book[0] < epoch_booked[1] : 
                            f_in = 1 
                        if  epoch_book[1] > epoch_booked[0] and epoch_book[1] < epoch_booked[1] : 
                            f_out = 1 
                        if  epoch_book[0] < epoch_booked[0] and epoch_book[1] > epoch_booked[1] : 
                            f_cover = 1 
                        if f_in or f_out or f_cover == 1: 
                            avaliable = '0' 
                        print("{} {} {} {}".format(epoch_book[0],epoch_book[1],epoch_booked[0],epoch_booked[1]))
                        print("{} {} {}".format(f_in,f_out,f_cover))
                    code += avaliable

            epoch_checkin = datetime.datetime(int(checkin[0:4]) ,int( checkin[5:7]) , int(checkin[8:10]) , 0 , 0).timestamp()
            # messages.success(request, f'Add room in cart Successsfully!')
            urlroom = ["/media/topview/"+code+".jpg"]
            button = code
            print(code)
            # return redirect('bookroom')

    else:
        form = BookingForm()
    context = { 'form': form,
                'urllist': urlroom,
                'button': button,
                'checkin': checkin,
                'checkout': checkout,
                }
    return render(request, "book_site.html",context)

@login_required
def food_buy(request):
    user = request.user
    if 'buy' in request.POST:
        form = BuyForm(request.POST)
        if form.is_valid():
            title = request.POST.get('title')
            quantity = form.cleaned_data['quantity']
            menu = Menu.objects.get(title=title)
            unit_price = menu.unit_price
            if Cart.objects.filter(user=user,menu=menu):
                UserCart = Cart.objects.get(user=user,menu=menu)
                Total_Quantity = UserCart.quantity + quantity
                UserCart.quantity = Total_Quantity
                UserCart.total_price = Total_Quantity*unit_price
                UserCart.save()
            else:
                UserCart = Cart(user=user,menu=menu,quantity=quantity,total_price=quantity*unit_price)
                UserCart.save()
            messages.success(request, f'Add {quantity} {title} in cart Successsfully!')
            return redirect('foodbuy')

    else:
        form = BuyForm()

    allmenu = Menu.objects.all()
    context = { 'form': form,
                'menulist':allmenu ,
                }
    return render(request, "buy_site.html",context)

@login_required
def cart(request):
    user = request.user
    if 'update' in request.POST:
        form = UpdateForm(request.POST)
        if form.is_valid():
            title = request.POST.get('title')
            quantity = form.cleaned_data['update_quantity']
            menu = Menu.objects.get(title=title)
            unit_price = menu.unit_price
            UserCart = Cart.objects.get(user=user,menu=menu)
            if quantity != 0:
                UserCart.quantity = quantity
                UserCart.total_price = quantity*unit_price
                UserCart.save()
                messages.success(request, f'Change quantity of {title} to {quantity} Successsfully!')
            else:
                UserCart.delete()
                messages.success(request, f'Delete {title} in cart Successsfully!')
            return redirect('cart')

    if 'check_bill' in request.POST:
        return redirect('payment')

    if 'cancel' in request.POST:
        idbooking = request.POST.get('idbooking')
        UserBooking = Booking.objects.get(id=idbooking)
        title = UserBooking.room.title
        checkin = UserBooking.checkin
        UserBooking.delete()
        messages.success(request, f'Delete Booking room "{title}" at {checkin} in cart Successsfully!')
        return redirect('cart')

    else:
        form = UpdateForm()

    allmenu = Cart.objects.filter(user=user)
    allbooking = Booking.objects.filter(user=user)
    allorder = Ordercart.objects.filter(user=user)
    menufood = []
    menudessert = []
    menubeverage = []
    for i in allmenu:
        if i.menu.type == "F":
            menufood.append(i)
        if i.menu.type == "D":
            menudessert.append(i)
        if i.menu.type == "B":
            menubeverage.append(i)
    context = { 'form': form,
                'bookinglist': allbooking ,
                'lenbooking': len(allbooking) ,
                'lencart': len(allmenu),
                'foodlist': menufood ,
                'lenfood': len(menufood),
                'dessertlist': menudessert ,
                'lendessert': len(menudessert),
                'beveragelist': menubeverage ,
                'lenbeverage': len(menubeverage),
                'orderlist': allorder ,
                'lenorder': len(allorder),
                }
    return render(request, "cart_site.html",context)

@login_required
def payment(request):
    user = request.user
    bill = 0
    for i in Cart.objects.filter(user=user):
        bill += i.total_price
    for i in Booking.objects.filter(user=user):
        bill += i.total_price

    account_ = "0951847769"
    current_time = str(datetime.datetime.now()).replace(" ","_").replace(":","-").replace(".","-")
    path = 'media/qrcode'+user.username # edit 
    if os.path.isdir(path):
        pass
    else:
        os.mkdir(path)
    path = 'media/qrcode'+user.username+'/'+current_time+'.png' # edit 
    money_ = str(bill)
    currency_ = "THB"
    qr_code(account=account_, one_time=True, path_qr_code = path ,country="TH",money=money_,currency=currency_)

    urlqr = ["/media/qrcode"+user.username+"/"+current_time+".png"] # call Urls qr_code 

    if 'submit' in request.POST:
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            bank = form.cleaned_data['bank']
            time = form.cleaned_data['datetime'].strftime("%d %m %Y %H:%M")
            if time[0] == "0":
                time = time[1:len(time)]
            slip = form.cleaned_data['slip']
            Order = Ordercart(user=user,placed_at=time,slip=slip,total_price=bill,payment_status="P")
            Order.save()
            path = 'media/slip/'+str(slip) # edit 
            print(path)
            img = cv.imread(path , cv.IMREAD_UNCHANGED )
            ret , thresh = cv.threshold(img, 170, 255, cv.THRESH_BINARY)
            bank_acc = bank
            image = thresh
            dt = time
            name_acc =  ['นายนีบุณ บุญประกอบ' , 'นายนิบุณ บุญประกอบ']
            amount = str(bill)+'.00 บาท'
            print("{} {} {}".format(bank,time,slip))
            status = Bp.check_all(bank = bank_acc,
                img_upload = image,
                date_time = dt ,
                name = name_acc , 
                amount = amount,)
            print(status)
            # print(Bp.kbank(Slip_kbank = thresh))
            if status:
                Order.payment_status = "C"
                Order.save()
            messages.success(request, f'Payment Successsfully!')
            return redirect('cart') 

    else:
        form = PaymentForm()

    allorder = Ordercart.objects.filter(user=user)
    context = { 'form': form,
                'urllist': urlqr,
                'orderlist':allorder,
                'bill':bill,
            }
    return render(request, "payment_site.html",context)

@api_view()
def product_list(request):
    return Response('ok')

@api_view()
def product_detail(request, id):
    return Response(id)