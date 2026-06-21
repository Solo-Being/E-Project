from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

def home(request):
    head = Product.objects.all()[:3]
    return render(request, 'home.html', {'head': head})

def products(request):
    query=request.GET.get('q')
    product=Product.objects.all()
    filteredProduct=None
    if query:
        filteredProduct=Product.objects.filter(
            c_desc__icontains=query
        ) | Product.objects.filter(
            category__category__icontains=query
        )
    elif query == '':
        return redirect(home)
    return render(request,'products.html', {'data':filteredProduct, 'query':query, 'product':product})

  
def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )
        return redirect('contact')
    return render(request, 'contact.html')

def details(request, id):
    item = Product.objects.get(pk=id)
    wished = False
    if request.user.is_authenticated:
        wished = Wishlist.objects.filter(
            product=item,
            user=request.user
            )
    return render(request, 'details.html', {'item': item,'wished': wished})

@login_required
def cart(request,id):
    product=Product.objects.get(pk=id)
    cart_item,created=Cart.objects.get_or_create(product=product, user=request.user)
    if not created:
        cart_item.quantity+=1
        cart_item.save()
    return redirect('cart_page')

@login_required
def cart_page(request):
    item=Cart.objects.filter(user=request.user)
    total=0
    for i in item:
        total+=i.total_price()
    return render(request,'cart.html',{'item':item,'total':total})

from django.contrib import messages  
from .forms import CreateUserForm    

def user_register(request):   
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            return redirect('Login')  
        else:
            print(form.errors)
    else:
        form = CreateUserForm()  
        
    return render(request,'signup.html',{'form': form}) 


from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def login_form(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                messages.success(request,f'Logged in as {username}!')
                return redirect('home')    
    return render(request,'login.html')

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    messages.success(request,f'Successfully Logged Out!')
    return redirect('home')

def about(request):
    return render(request,'about.html')

def casual(request):
    category=Category.objects.get(category='Casual')
    product=Product.objects.filter(category=category)
    return render(request,'products.html',{'data':product})

def vintage(request):
    category=Category.objects.get(category='Vintage')
    product=Product.objects.filter(category=category)
    return render(request,'products.html',{'data':product})

def luxury(request):
    category=Category.objects.get(category='Luxury')
    product=Product.objects.filter(category=category)
    return render(request,'products.html',{'data':product})

@login_required
def buy(request,id):
    cart_item=Cart.objects.get(pk=id, user=request.user)
    order=Order()
    order.user=cart_item.user
    order.product=cart_item.product
    order.quantity=cart_item.quantity
    order.save()
    cart_item.delete()
    return redirect('Orders')

@login_required
def order(request):
    order_item=Order.objects.filter(user=request.user)
    order_data=[]
    grand_total = 0
    for i in order_item:
        item=OrderItem.objects.filter(order=i)
        total = 0
        for j in item:
            total += j.quantity * j.product.c_price
        grand_total += total
        
        order_data.append({
            'id':i.id,
            'date_time':i.date_time,
            'items':item,
            'total':total,
            'address':i.address
        })
        
    count=order_item.count()
    return render(request,'order.html',{'orders':order_data,'grand_total':grand_total,'count':count})

def cart_increment(request,id):
    cart_item=Cart.objects.get(pk=id)
    cart_item.quantity+=1
    cart_item.save()
    return redirect('cart_page')

def cart_decrement(request,id):
    cart_item=Cart.objects.get(pk=id)
    cart_item.quantity-=1
    cart_item.save()
    if cart_item.quantity==0:
        cart_item.delete()
    return redirect('cart_page')

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    order_item = Order.objects.filter(user=request.user)
    cart_item = Cart.objects.filter(user=request.user)
    order_data = []
    grand_total = 0
    for i in order_item:
        item = OrderItem.objects.filter(order=i)
        total = 0
        for j in item:
            total += j.quantity * j.product.c_price
        grand_total += total

        order_data.append({
            'id': i.id,
            'date_time': i.date_time,
            'items': item,
            'total': total,
            'address': i.address
        })
    count = order_item.count()
    cart_count = cart_item.count()
    return render(request, 'profile.html', {'count': count,
        'c_count': cart_count,
        'orders': order_data,
        'grand_total': grand_total,
        'profile': profile
    })

def address(request,id=None):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone=request.POST['phone']
        alt_phone=request.POST['alt_phone']
        addres=request.POST['address']
        city=request.POST['city']
        pin=request.POST['pin_code']
        state=request.POST['state']
        landmark=request.POST['landmark']
        cod=request.POST['cod']
    
        address_obj=Address()
        address_obj.first_name=first_name
        address_obj.last_name=last_name
        address_obj.user=request.user
        address_obj.user=request.user
        address_obj.phone=phone
        address_obj.alt_phone=alt_phone
        address_obj.adress=addres
        address_obj.city=city
        address_obj.pin_code=pin
        address_obj.state=state
        address_obj.land_mark=landmark
        address_obj.payment=cod
    
        address_obj.save()
        
        if id is not None:

            item = Cart.objects.get(pk=id)
            
            order = Order()
            order.user=request.user
            order.address=address_obj
            order.save()
            
            order_item = OrderItem()
            order_item.order=order
            order_item.product=item.product
            order_item.quantity=item.quantity
            order_item.save()
            
            item.delete()

        else:
            cart_items = Cart.objects.filter(user=request.user)
            order = Order()
            order.user=request.user
            order.address=address_obj
            order.save()

            for item in cart_items:
                order_item = OrderItem()
                order_item.order=order
                order_item.product=item.product
                order_item.quantity=item.quantity
                order_item.save()
            cart_items.delete()
            
        head = {
            'head': Product.objects.all()[:3],
            'ordered': True
        }

        return render(request,'home.html',head)
    return render(request,'Address.html',{'product_id': id})
        
def place_order(request, id=None):
    cart_item=Cart.objects.filter(user=request.user)
    if not cart_item.exists():
        return render(request,'Cart.html',{'order_error':True})
        
    if id is not None:
        return redirect('Address', id=id)

    return redirect('Address')

def  edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.first_name =request.POST.get('first_name')
        profile.last_name =request.POST.get('last_name')
        profile.email =request.POST.get('email')
        profile.phone =request.POST.get('phone')
        profile.bio = request.POST.get('bio')
        image = request.FILES.get('profile_pic')
        if image:
            profile.profile_image = image 
        profile.save()
        return redirect('Profile')
    return render(request,'edit.html')

@login_required
def wish(request,id):
    product = Product.objects.get(pk=id)
    item, created = Wishlist.objects.get_or_create(
        product=product,
        user = request.user
    )
    if not created:
        item.delete()
    return redirect('details',id=id)

@login_required
def wish_list(request):
    product = Wishlist.objects.filter(user=request.user)
    return render(request,'wishlist.html',{'product':product})

def removefc(request, item_id):
    cart_item = Cart.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart_page')