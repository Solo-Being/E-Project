from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    category=models.CharField(max_length=100)
    def __str__(self):             
        return self.category
    
    
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    c_image=models.ImageField(upload_to='products')
    c_desc=models.TextField(max_length=500)
    c_price=models.IntegerField()
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.c_price
    
    def __str__(self):
        return self.user.username
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150)
    phone=models.IntegerField()
    alt_phone=models.IntegerField()
    adress=models.TextField(max_length=250)
    city=models.CharField(max_length=50)
    pin_code=models.IntegerField(max_length=6)
    state=models.CharField(max_length=100)
    land_mark=models.TextField(max_length=250,null=True,blank=True)
    payment=models.CharField(default='COD')

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE,null=True, blank=True)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
from django.contrib.auth.models import User
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30,blank=True)
    last_name = models.CharField(max_length=30,blank=True)
    phone = models.IntegerField(null=True,blank=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/',null=True,blank=True)
    
    def __str__(self):
        return self.user.username 

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)