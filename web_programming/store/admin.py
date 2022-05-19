from django.contrib import admin,messages
from django.contrib.contenttypes.admin import GenericTabularInline

from tags.models import TaggedItem
from . import models
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.db.models import Count

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10','Low')   #first actual filter second show
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)  #inventory less than 10

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem

@admin.register(models.Product)         #class นี้เป็นของ product ทำให้ไม่ต้องมี line ด้ายล่าง
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']   #ต้องไป search tilte ใน collection ให้ก่อน
    prepopulated_fields = {
        'slug': ['title']   # slug follow title when type title
    }
    actions = ['clear_inventory']
    inlines = [TagInline]
    list_display = ['title','unit_price','inventory_status','collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection','last_update',InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title__istartswith']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')     #sorting by inventory
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)  # ต้องเก็บไว้ในตัวเเปรไม่งั้นจะโชวค่าออกมา
        self.message_user(
            request,
            f'{updated_count} products were successfully updated',
            messages.SUCCESS
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership','orders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name','last_name']
    search_fields = ['first_name__istartswith','last_name__istartswith']    #search bar ด้วยตัวเเรก เเละไม่สน capital โดยใช้ i

    @admin.display(ordering='orders_count')
    def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')  #เขียน str ให้เหมือน url
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            })
            )   
        return format_html('<a href="{}">{}</a>',url,customer.orders_count) #url เช่น google.com

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count = Count('order')
        )

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    search_fields = ['title__istartswith']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')  #เขียน str ให้เหมือน url
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            })
            )   
        return format_html('<a href="{}">{}</a>',url,collection.products_count) #url เช่น google.com

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count('product')
        )

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at','customer']

# admin.site.register(models.Product,ProductAdmin)    no need

@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title','unit_price','type']
    list_editable = ['unit_price']
    list_filter = ['type']
    list_per_page = 10
    search_fields = ['title__istartswith']

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user','menu','quantity','total_price']
    list_editable = ['quantity','total_price']
    # list_filter = ['type']
    list_per_page = 10
    # search_fields = ['title__istartswith']

@admin.register(models.Ordercart)
class OrderCartAdmin(admin.ModelAdmin):
    list_display = ['id','placed_at','user','total_price','slip','payment_status']
    list_editable = ['payment_status']
    # list_filter = ['type']
    list_per_page = 10
    # search_fields = ['title__istartswith']

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['title','people','unit_price']
    list_editable = ['unit_price']
    list_per_page = 10
    
@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id','user','room','checkin','checkout','day','total_price']
    list_per_page = 10

