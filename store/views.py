from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

from .models import Cartitems, Customer, Product, Cart

from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

import json

import requests

def store(request):
    cart = None
    cartitems = None
    
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            cart, created = Cart.objects.get_or_create(customer=customer, completed=False)
            cartitems = cart.cartitems_set.all()
        except Customer.DoesNotExist:
            cart = None
            cartitems = None
    
    products = Product.objects.all()
    paginator = Paginator(products, 5)
    pageNumber = request.GET.get('page')
    
    try:
        products = paginator.page(pageNumber)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products, 
        'cart': cart,
        'cartitems': cartitems
    }
    
    return render(request, 'store.html', context)

def cart(request):
    # Nếu chưa đăng nhập, chuyển đến trang login
    if not request.user.is_authenticated:
        return redirect('login')

    customer = request.user.customer
    cart, created = Cart.objects.get_or_create(customer = customer, completed = False)
    cartitems = cart.cartitems_set.all()

    return render(request, 'cart.html', {'cartitems' : cartitems, 'cart':cart})

def checkout(request):
    # Nếu chưa đăng nhập, chuyển đến trang login
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,'checkout.html',{})

def updateCart(request):

    data = json.loads(request.body)

    productId = data["productId"]

    action = data["action"]

    product = Product.objects.get(id=productId)

    customer = request.user.customer

    cart, created = Cart.objects.get_or_create(customer = customer, completed = False)

    cartitem, created = Cartitems.objects.get_or_create(cart = cart, product = product)


    if action == "add":

        cartitem.quantity += 1

        cartitem.save()

   


    return JsonResponse("Cart Updated", safe = False)


def updateQuantity(request):
    data = json.loads(request.body)
    
    # Xử lý cả 2 format cũ và mới
    if 'itemId' in data and 'quantity' in data:
        # Format mới từ cart.html
        itemId = data['itemId']
        quantity = data['quantity']
        
        cartitem = Cartitems.objects.get(id=itemId)
        cartitem.quantity = quantity
        cartitem.save()
    else:
        # Format cũ từ cart.js
        quantityFieldValue = data['qfv']
        quantityFieldProduct = data['qfp']

        product = Cartitems.objects.filter(product__name=quantityFieldProduct).last()
        product.quantity = quantityFieldValue
        product.save()

    return JsonResponse("Quantity updated", safe=False)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('store')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Chuyển hướng đến trang mà người dùng muốn truy cập
            next_url = request.GET.get('next', 'store')
            if next_url != 'store':
                return redirect(next_url)
            return redirect('store')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
    
    return render(request, 'login.html', {})


def logoutPage(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('store')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        name = request.POST.get('name')
        
        if password1 != password2:
            messages.error(request, 'Mật khẩu không khớp!')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Tên đăng nhập đã tồn tại!')
            return redirect('register')
        
        user = User.objects.create_user(username=username, password=password1, email=email)
        
        # Tạo Customer profile
        customer = Customer.objects.create(user=user, name=name, email=email)
        
        messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
        return redirect('login')
    
    return render(request, 'register.html', {})