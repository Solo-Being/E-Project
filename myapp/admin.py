from django.contrib import admin
from .models import *

class Product_det(admin.ModelAdmin):
    list_display=('category','c_image','c_desc','c_price')

class ContactM(admin.ModelAdmin):
    list_display=('name','email','subject','message')   
    
class Orderdt(admin.ModelAdmin):
    list_display=('order','product','quantity')  

class Wishdt(admin.ModelAdmin):
    list_display=('user','product')  
    
class Orderdet(admin.ModelAdmin):
    list_display=('user','date_time','address') 

# Register your models here.

admin.site.register(Category)
admin.site.register(Product,Product_det)
admin.site.register(Cart)
admin.site.register(Order,Orderdet)
admin.site.register(OrderItem,Orderdt)
admin.site.register(Wishlist,Wishdt)
admin.site.register(ContactMessage,ContactM)