from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+') #circular denpency เเก้ได้โดยใช้ '' เเต่เมื่อจำเป็นเท่านั้น เพราะไม่อัพเดท -- relate name + เพื่อไม่ให้ reverse ทับกัน collection.product, product.collection
    
    def __str__(self) -> str:   #show title name of object
        return self.title
    
    class Meta:                 #sorting by title name
        ordering = ['title']

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT) #1 collection many Product -- accident delete collection จะไม่ delete all product in collection
    promotion = models.ManyToManyField(Promotion, blank=True)

    def __str__(self) -> str:   #show title name of object
        return self.title
    
    class Meta:                 #sorting by title name
        ordering = ['title']

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)

    def __str__(self) -> str:   #show title name of object
        return f'{self.first_name} {self.last_name}'
    
    class Meta:                 #sorting by title name
        ordering = ['first_name','last_name']



class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.PositiveIntegerField()
    #customer = models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True) #set_null - เมื่อ deleteลูกค้า address ไม่หาย เเต่ custumer จะขึ้น null, Protect - ต้อง delete child first,cascade - ลบหายทั้งคู่, set primary key เนื่องจาก 1ต่อ1 เท่านั้น duplicate ไม่ได้
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE) #1customer many address

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING,'Pending'),
        (PAYMENT_STATUS_COMPLETE,'Complete'),
        (PAYMENT_STATUS_FAILED,'Failed'),
    ]

    placed_at = models.DateField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICES,default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Menu(models.Model):
    TYPE_FOOD = 'F'
    TYPE_DESSERT = 'D'
    TYPE_BEVERAGE = 'B'
    TYPE_CHOICES = [
        (TYPE_FOOD,'Food'),
        (TYPE_DESSERT,'Dessert'),
        (TYPE_BEVERAGE,'Beverage'),
    ]
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=1,choices=TYPE_CHOICES,default=TYPE_FOOD)
    photo = models.ImageField(upload_to="menu/", null=True, blank=True)
    unit_price = models.DecimalField(
                max_digits=6, 
                decimal_places=2,
                validators=[MinValueValidator(1)])


    def __str__(self) -> str:   #show title name of object
        return self.title
    
    class Meta:                 #sorting by title name
        ordering = ['title']

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT, null=True)
    quantity = models.PositiveSmallIntegerField()
    total_price = models.PositiveSmallIntegerField()

class Ordercart(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING,'Pending'),
        (PAYMENT_STATUS_COMPLETE,'Complete'),
        (PAYMENT_STATUS_FAILED,'Failed'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    placed_at = models.DateTimeField(auto_now_add=True)
    slip = models.ImageField(upload_to="slip/", null=True, blank=True)
    total_price = models.PositiveSmallIntegerField()
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICES,default=PAYMENT_STATUS_PENDING)

class Room(models.Model):
    PEOPLE_2 = '2'
    PEOPLE_4 = '4'
    PEOPLE_CHOICES = [
        (PEOPLE_2,'2 persons'),
        (PEOPLE_4,'4 persons'),
    ]

    title = models.CharField(max_length=255)
    people = models.CharField(max_length=1,choices=PEOPLE_CHOICES,default=PEOPLE_2)
    unit_price = models.DecimalField(
                max_digits=8, 
                decimal_places=2,
                validators=[MinValueValidator(1)])
    photo = models.ImageField(upload_to="room/", null=True, blank=True)

    def __str__(self) -> str:   #show title name of object
        return self.title
    
    class Meta:                 #sorting by title name
        ordering = ['people']

class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    checkin = models.DateField(auto_now=False, auto_now_add=False)
    checkout = models.DateField(auto_now=False, auto_now_add=False)
    day = models.PositiveSmallIntegerField()
    total_price = models.PositiveSmallIntegerField()

    

