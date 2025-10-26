from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from itertools import product

from .models import Cartitems, Customer, Product, Cart

from django.http import JsonResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.http import require_POST


# Create your views here.



def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    customer = request.user.customer
    cart = Cart.objects.filter(customer=customer, completed=False).first()
    cartitems = cart.cartitems_set.all() if cart else []
    return render(request, 'cart.html', {'cartitems': cartitems})



def checkout(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_items')
        cartitems = Cartitems.objects.filter(id__in=selected_ids)
        subtotal = sum(item.product.price * item.quantity for item in cartitems)
        shipping = 37700 if cartitems else 0
        total = subtotal + shipping
    else:
        cartitems = []
        subtotal = 0
        shipping = 0
        total = 0
    user = request.user
    return render(request, 'checkout.html', {
        'cartitems': cartitems,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'user': user,
    })




# Create your views here.

def store(request):

    products = Product.objects.all()

    paginator = Paginator(products, 4)

    pageNumber = request.GET.get('page')

    try:

        products = paginator.page(pageNumber)

    except PageNotAnInteger:

        products = paginator.page(1)

    except EmptyPage:

        products = paginator.page(paginator.num_pages)


    cart = None

    if request.user.is_authenticated:

        customer = request.user.customer

        cart = Cart.objects.filter(customer=customer, completed=False).first()

        if cart is None:

            cart = Cart.objects.create(customer=customer, completed=False)

    return render(request, 'store.html', {'products': products, 'cart':cart})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('store')
        else:
            return render(request, 'login.html', {'error': 'Sai thông tin đăng nhập'})
    return render(request, 'login.html')

def add_to_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        customer = request.user.customer
        cart = Cart.objects.filter(customer=customer, completed=False).first()
        if cart is None:
            cart = Cart.objects.create(customer=customer, completed=False)
        cart_item, created = Cartitems.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@require_POST
def increase_cartitem(request, item_id):
    item = Cartitems.objects.get(id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart')

@require_POST
def decrease_cartitem(request, item_id):
    item = Cartitems.objects.get(id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')

@require_POST
def reset_cart_quantities(request):
    if not request.user.is_authenticated:
        return redirect('login')
    customer = request.user.customer
    cart = Cart.objects.filter(customer=customer, completed=False).first()
    if cart:
        for item in cart.cartitems_set.all():
            item.quantity = 1
            item.save()
    return redirect('cart')

@require_POST
def remove_cartitem(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login')
    item = Cartitems.objects.get(id=item_id)
    item.delete()
    return redirect('cart')


