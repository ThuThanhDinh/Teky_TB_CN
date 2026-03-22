from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from itertools import product
from django.db import models
from django.db.models import Q

from .models import Cartitems, Customer, Product, Cart

from django.http import JsonResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone


# Create your views here.



def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    customer = request.user.customer
    cart = Cart.objects.filter(customer=customer, completed=False).first()
    cartitems = cart.cartitems_set.all() if cart else []
    # compute subtotal
    subtotal = sum(item.product.price * item.quantity for item in cartitems) if cartitems else 0

    return render(request, 'cart.html', {
        'cartitems': cartitems,
        'subtotal': subtotal,
    })

def product_detail(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    product = Product.objects.get(id=product_id)
    
    # Handle review submission
    if request.method == 'POST' and 'review_rating' in request.POST:
        rating = request.POST.get('review_rating')
        content = request.POST.get('review_content', '')
        Comment.objects.create(
            product=product,
            user=request.user,
            rating=int(rating),
            content=content
        )
        return redirect('product_detail', product_id=product_id)
    
    # Get reviews and calculate average rating
    from django.db.models import Avg
    reviews = product.comments.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    rating_count = reviews.count()
    
    # Get shop of this product
    shop = product.shop if hasattr(product, 'shop') else None
    
    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'rating_count': rating_count,
        'shop': shop,
    })

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    customer = user.customer

    cart = Cart.objects.filter(customer=customer, completed=False).first()
    cartitems = cart.cartitems_set.all() if cart else []

    subtotal = sum(item.product.price * item.quantity for item in cartitems) if cartitems else 0
    shipping = 37700 if cartitems else 0
    
    # Get applicable vouchers
    from .context_processors import voucher_context
    ctx = voucher_context(request)
    applicable_vouchers = ctx.get('applicable_vouchers', [])
    
    # Initialize discount variables
    discount_amount = 0
    voucher_name = ''
    selected_voucher = None
    
    # Handle POST from cart page (voucher selection)
    if request.method == 'POST':
        selected_voucher_code = request.POST.get('selected_voucher', '').strip()
        if selected_voucher_code:
            try:
                selected_voucher = Voucher.objects.get(code=selected_voucher_code, enabled=True)
                # Check if voucher is applicable (min_purchase requirement)
                if subtotal >= selected_voucher.min_purchase:
                    # Calculate discount
                    if selected_voucher.fixed_amount:
                        # Fixed amount discount
                        discount_amount = selected_voucher.fixed_amount
                    elif selected_voucher.percent and selected_voucher.percent > 0:
                        # Percentage discount
                        discount_amount = (subtotal * selected_voucher.percent) / 100
                        # Apply max_amount limit if exists
                        if selected_voucher.max_amount and discount_amount > selected_voucher.max_amount:
                            discount_amount = selected_voucher.max_amount
                    else:
                        discount_amount = 0
                    
                    voucher_name = selected_voucher.code
                else:
                    # Voucher doesn't meet minimum purchase requirement
                    selected_voucher = None
                    discount_amount = 0
                    voucher_name = ''
            except Voucher.DoesNotExist:
                selected_voucher = None
                discount_amount = 0
                voucher_name = ''
    
    # Ensure discount doesn't exceed subtotal
    if discount_amount > subtotal:
        discount_amount = subtotal
    
    # Handle free shipping
    if selected_voucher and selected_voucher.free_shipping:
        shipping = 0
    
    total = subtotal + shipping - discount_amount
    
    # Lấy địa chỉ mặc định của user
    default_address = customer.addresses.filter(is_default=True).first()
    if not default_address:
        default_address = customer.addresses.first()  # Lấy địa chỉ đầu tiên nếu không có mặc định

    return render(request, 'checkout.html', {
        'cartitems': cartitems,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'user': user,
        'customer': customer,
        'discount_amount': discount_amount,
        'voucher_name': voucher_name,
        'applicable_vouchers': applicable_vouchers,
        'selected_voucher': selected_voucher,
        'default_address': default_address,
    })




# Create your views here.

def store(request):
    """Hiển thị tất cả sản phẩm với sidebar lọc và voucher, phần dưới hiển thị cửa hàng"""
    # Support search for products or shops
    query = request.GET.get('q', '')
    search_type = request.GET.get('search_type', 'product')
    
    # If searching for shops, redirect to shop list or filter shops
    if query and search_type == 'shop':
        # Filter shops by name
        shops_qs = Shop.objects.filter(name__icontains=query, is_active=True)
        # Get products normally (no product search when searching shops)
        products_qs = Product.objects.all()
    else:
        # Normal product search
        if query:
            products_qs = Product.objects.filter(name__icontains=query)
        else:
            products_qs = Product.objects.all()
        shops_qs = Shop.objects.filter(is_active=True)

    # Filter by price range (only for products)
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        products_qs = products_qs.filter(price__gte=int(price_min))
    if price_max:
        products_qs = products_qs.filter(price__lte=int(price_max))

    # Filter by rating (average rating >= selected)
    rating_min = request.GET.get('rating')
    if rating_min:
        from django.db.models import Avg
        # Products with average rating >= rating_min
        products_qs = products_qs.annotate(avg_rating=Avg('comments__rating')).filter(avg_rating__gte=float(rating_min))

    paginator = Paginator(products_qs, 8)
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
    
    # Get applicable vouchers for sidebar
    from .context_processors import voucher_context
    ctx = voucher_context(request)
    applicable_vouchers = ctx.get('applicable_vouchers', [])
    
    # Get shops for bottom section (limit to 8 shops, or filtered shops if searching)
    if query and search_type == 'shop':
        shops = shops_qs.order_by('-created_at')[:8]
    else:
        shops = Shop.objects.filter(is_active=True).order_by('-created_at')[:8]

    # Get featured products: products with most reviews, prioritizing 5-star reviews
    from django.db.models import Count, Avg
    featured_products = Product.objects.annotate(
        total_reviews=Count('comments'),
        five_star_reviews=Count('comments', filter=Q(comments__rating=5)),
        avg_rating=Avg('comments__rating')
    ).filter(total_reviews__gt=0).order_by('-five_star_reviews', '-total_reviews')[:10]

    # Group featured products into slides of 4
    featured_slides = []
    products_list = list(featured_products)
    for i in range(0, len(products_list), 4):
        featured_slides.append(products_list[i:i+4])

    # total matches (across all pages) when searching
    results_count = products_qs.count() if query else products_qs.count()
    return render(request, 'store.html', {
        'products': products, 
        'cart': cart, 
        'query': query,
        'search_type': search_type,
        'results_count': results_count,
        'price_min': price_min or '',
        'price_max': price_max or '',
        'rating': rating_min or '',
        'applicable_vouchers': applicable_vouchers,
        'shops': shops,
        'featured_slides': featured_slides,
    })


def shop_detail(request, shop_id):
    """Hiển thị chi tiết cửa hàng và danh sách sản phẩm"""
    try:
        shop = Shop.objects.get(id=shop_id, is_active=True)
    except Shop.DoesNotExist:
        messages.error(request, 'Cửa hàng không tồn tại hoặc đã đóng cửa.')
        return redirect('store')
    
    # Support simple search via GET parameter 'q'
    query = request.GET.get('q', '')
    if query:
        products_qs = shop.products.filter(name__icontains=query)
    else:
        products_qs = shop.products.all()

    # Filter by price range
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        products_qs = products_qs.filter(price__gte=int(price_min))
    if price_max:
        products_qs = products_qs.filter(price__lte=int(price_max))

    # Filter by rating
    rating_min = request.GET.get('rating')
    if rating_min:
        from django.db.models import Avg
        products_qs = products_qs.annotate(avg_rating=Avg('comments__rating')).filter(avg_rating__gte=float(rating_min))

    paginator = Paginator(products_qs, 8)
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

    # Calculate average rating for shop
    from django.db.models import Avg
    avg_rating_result = shop.products.aggregate(Avg('comments__rating'))
    avg_rating = avg_rating_result.get('comments__rating__avg') or 0

    results_count = products_qs.count() if query else products_qs.count()
    return render(request, 'shop_detail.html', {
        'shop': shop,
        'products': products,
        'cart': cart,
        'query': query,
        'results_count': results_count,
        'price_min': price_min or '',
        'price_max': price_max or '',
        'rating': rating_min or '',
        'avg_rating': avg_rating,
    })


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

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('store')

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

@require_POST
def place_order(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    customer = request.user.customer
    cart = Cart.objects.filter(customer=customer, completed=False).first()
    
    if cart:
        # Tính toán các số tiền
        cartitems = cart.cartitems_set.all()
        subtotal = sum(item.product.price * item.quantity for item in cartitems) if cartitems else 0
        shipping = 37700 if cartitems else 0
        
        # Xử lý voucher
        selected_voucher_code = request.POST.get('selected_voucher', '').strip()
        discount_amount = 0
        voucher_code = None
        
        if selected_voucher_code:
            try:
                selected_voucher = Voucher.objects.get(code=selected_voucher_code, enabled=True)
                if subtotal >= selected_voucher.min_purchase:
                    # Calculate discount
                    if selected_voucher.fixed_amount:
                        discount_amount = selected_voucher.fixed_amount
                    elif selected_voucher.percent and selected_voucher.percent > 0:
                        discount_amount = (subtotal * selected_voucher.percent) / 100
                        if selected_voucher.max_amount and discount_amount > selected_voucher.max_amount:
                            discount_amount = selected_voucher.max_amount
                    
                    # Handle free shipping
                    if selected_voucher.free_shipping:
                        shipping = 0
                    
                    voucher_code = selected_voucher.code
            except Voucher.DoesNotExist:
                pass
        
        # Ensure discount doesn't exceed subtotal
        if discount_amount > subtotal:
            discount_amount = subtotal
        
        final_total = subtotal + shipping - discount_amount
        
        # Lưu địa chỉ giao hàng
        address = request.POST.get('shipping_address', '')
        city = request.POST.get('shipping_city', '')
        state = request.POST.get('shipping_state', '')
        zipcode = request.POST.get('shipping_zipcode', '')
        
        if address and city and state:
            ShippingAddress.objects.create(
                customer=customer,
                cart=cart,
                address=address,
                city=city,
                state=state,
                zipcode=zipcode
            )
        
        # Lưu phương thức thanh toán
        payment_method = request.POST.get('payment_method', 'cod')
        if payment_method not in ['cod', 'bank']:
            payment_method = 'cod'
        
        # Lưu thông tin voucher và các số tiền vào cart
        cart.voucher_code = voucher_code
        cart.subtotal = subtotal
        cart.discount_amount = discount_amount
        cart.shipping = shipping
        cart.final_total = final_total
        cart.payment_method = payment_method
        
        # Đánh dấu cart đã hoàn thành và lưu thời gian hoàn tất
        cart.completed = True
        cart.completed_at = timezone.now()
        cart.save()
        
        # Thông báo thành công
        messages.success(request, 'Cảm ơn bạn! Đơn hàng của bạn đã được đặt thành công.')
        
        # Redirect về trang chủ với thông báo
        return redirect('store')
    
    return redirect('cart')


def purchase_history(request):
    if not request.user.is_authenticated:
        return redirect('login')
    customer = request.user.customer
    # completed carts are treated as orders
    orders = Cart.objects.filter(customer=customer, completed=True).order_by('-id')
    # attach items and shipping info per order
    orders_data = []
    from .models import ShippingAddress
    for order in orders:
        items = order.cartitems_set.select_related('product').all()
        shipping = ShippingAddress.objects.filter(cart=order).first()
        
        # Get voucher info if exists
        voucher = None
        if order.voucher_code:
            try:
                voucher = Voucher.objects.get(code=order.voucher_code)
            except Voucher.DoesNotExist:
                pass
        
        # Use saved values if available, otherwise calculate
        subtotal = order.subtotal if order.subtotal > 0 else order.get_cart_total
        discount_amount = order.discount_amount if order.discount_amount > 0 else 0
        shipping_cost = order.shipping if order.shipping > 0 else 37700
        final_total = order.final_total if order.final_total > 0 else (subtotal + shipping_cost - discount_amount)
        
        orders_data.append({
            'order': order,
            'items': items,
            'total': final_total,  # Use final_total instead of get_cart_total
            'subtotal': subtotal,
            'discount_amount': discount_amount,
            'shipping_cost': shipping_cost,
            'voucher': voucher,
            'voucher_code': order.voucher_code,
            'item_count': order.get_itemtotal,
            'shipping': shipping,
        })

    return render(request, 'Purchase Log.html', {'orders': orders_data})


def vouchers_list(request):
    """Show all vouchers with details."""
    # context processor already provides `all_vouchers` and `user_rank` when user is authenticated
    # but to be safe, build a minimal list if not present
    vouchers = []
    if hasattr(request, 'user') and request.user.is_authenticated:
        # context processor will have populated all_vouchers
        vouchers = request.context.get('all_vouchers') if hasattr(request, 'context') else None
    # fallback: fetch from context processor directly
    from .context_processors import voucher_context
    ctx = voucher_context(request)
    vouchers = ctx.get('all_vouchers', [])
    user_rank = ctx.get('user_rank', '')
    return render(request, 'vouchers.html', {'vouchers': vouchers, 'user_rank': user_rank})


def voucher_detail(request, voucher_code):
    """Get voucher details as JSON for modal display."""
    try:
        voucher = Voucher.objects.get(code=voucher_code)
        from .context_processors import voucher_context
        ctx = voucher_context(request)
        user_rank = ctx.get('user_rank', '')
        
        # Check if voucher is applicable for user
        is_applicable = False
        if user_rank:
            is_applicable = any(r.name == user_rank for r in voucher.ranks.all())
        
        data = {
            'code': voucher.code,
            'desc': voucher.desc,
            'percent': voucher.percent,
            'fixed_amount': voucher.fixed_amount,
            'max_amount': voucher.max_amount,
            'min_purchase': voucher.min_purchase,
            'free_shipping': voucher.free_shipping,
            'enabled': voucher.enabled,
            'image': voucher.image.url if voucher.image else None,
            'is_applicable': is_applicable,
            'ranks': [r.name for r in voucher.ranks.all()],
        }
        return JsonResponse(data)
    except Voucher.DoesNotExist:
        return JsonResponse({'error': 'Voucher not found'}, status=404)


def profile(request):
    """Trang hồ sơ để quản lý địa chỉ giao hàng"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    customer = request.user.customer
    addresses = customer.addresses.all()
    
    return render(request, 'profile.html', {
        'customer': customer,
        'addresses': addresses,
    })


@require_POST
def add_address(request):
    """Thêm địa chỉ mới"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    customer = request.user.customer
    address = request.POST.get('address', '').strip()
    city = request.POST.get('city', '').strip()
    state = request.POST.get('state', '').strip()
    zipcode = request.POST.get('zipcode', '').strip()
    is_default = request.POST.get('is_default') == 'on'
    
    if address and city and state:
        # Nếu đặt làm mặc định, bỏ mặc định của các địa chỉ khác
        if is_default:
            customer.addresses.filter(is_default=True).update(is_default=False)
        
        UserAddress.objects.create(
            customer=customer,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode if zipcode else None,
            is_default=is_default
        )
        messages.success(request, 'Đã thêm địa chỉ mới thành công!')
    else:
        messages.error(request, 'Vui lòng điền đầy đủ thông tin địa chỉ.')
    
    return redirect('profile')


@require_POST
def edit_address(request, address_id):
    """Sửa địa chỉ"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    customer = request.user.customer
    try:
        user_address = UserAddress.objects.get(id=address_id, customer=customer)
    except UserAddress.DoesNotExist:
        messages.error(request, 'Địa chỉ không tồn tại.')
        return redirect('profile')
    
    address = request.POST.get('address', '').strip()
    city = request.POST.get('city', '').strip()
    state = request.POST.get('state', '').strip()
    zipcode = request.POST.get('zipcode', '').strip()
    is_default = request.POST.get('is_default') == 'on'
    
    if address and city and state:
        # Nếu đặt làm mặc định, bỏ mặc định của các địa chỉ khác
        if is_default:
            customer.addresses.filter(is_default=True).exclude(id=address_id).update(is_default=False)
        
        user_address.address = address
        user_address.city = city
        user_address.state = state
        user_address.zipcode = zipcode if zipcode else None
        user_address.is_default = is_default
        user_address.save()
        
        messages.success(request, 'Đã cập nhật địa chỉ thành công!')
    else:
        messages.error(request, 'Vui lòng điền đầy đủ thông tin địa chỉ.')
    
    return redirect('profile')


@require_POST
def delete_address(request, address_id):
    """Xóa địa chỉ"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    customer = request.user.customer
    try:
        user_address = UserAddress.objects.get(id=address_id, customer=customer)
        user_address.delete()
        messages.success(request, 'Đã xóa địa chỉ thành công!')
    except UserAddress.DoesNotExist:
        messages.error(request, 'Địa chỉ không tồn tại.')
    
    return redirect('profile')


@require_POST
def set_default_address(request, address_id):
    """Đặt địa chỉ làm mặc định"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    customer = request.user.customer
    try:
        user_address = UserAddress.objects.get(id=address_id, customer=customer)
        # Bỏ mặc định của các địa chỉ khác
        customer.addresses.filter(is_default=True).update(is_default=False)
        # Đặt địa chỉ này làm mặc định
        user_address.is_default = True
        user_address.save()
        messages.success(request, 'Đã đặt địa chỉ làm mặc định!')
    except UserAddress.DoesNotExist:
        messages.error(request, 'Địa chỉ không tồn tại.')
    
    return redirect('profile')


