from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Product, post,Order
from .forms import UserSignUpForm
from django.shortcuts import render, redirect,  get_object_or_404
from .forms import OrderForm
from django.utils import timezone


from django.contrib import messages
from .models import User
def members(request):
  template = loader.get_template('myfist.html')
  return HttpResponse(template.render())

def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())

def register(request):
  template = loader.get_template('register.html')
  return HttpResponse(template.render())

# def login(request):
#   template = loader.get_template('login.html')
#   return HttpResponse(template.render())

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username, password=password)
            messages.success(request, "Đăng nhập thành công!")
            return redirect('/trangchu')  # hoặc '/'
        except User.DoesNotExist:
            messages.error(request, "Sai tên đăng nhập hoặc mật khẩu.")
            return redirect('login')
    return render(request, "login.html")

def error(request):
  template = loader.get_template('error.html')
  return HttpResponse(template.render())



def success(request):
  template = loader.get_template('success.html')
  return HttpResponse(template.render())

def trangchu(request):
  template = loader.get_template('trangchu.html')
  return HttpResponse(template.render())

# def trangbanhang(request):
#   template = loader.get_template('trangbanhang.html')
#   productdata = Product.objects.all()
#   return HttpResponse(template.render())
def trangbanhang(request):
    template = loader.get_template('trangbanhang.html')
    productdata = Product.objects.all()
    context = {
        'products': productdata
    }
    return HttpResponse(template.render(context, request))
def post(request):
  template = loader.get_template('post.html')
  # postdata = post.objects.all()
  return HttpResponse(template.render())
 
def create(info):
  template = loader.get_template('info.html')
  return HttpResponse(template.render())

def login_success(info):
  template = loader.get_template('info.html')
  return HttpResponse(template.render())

def signUp(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  # Chuyển hướng sau khi đăng ký thành công
    else:
        form = UserSignUpForm()
    return render(request, 'register.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})



def order_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()
            return redirect('trangbanhang')  # Sau khi đặt hàng, chuyển về trang bán hàng
    else:
        form = OrderForm()

    return render(request, 'order.html', {'form': form, 'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart

    return redirect('trangbanhang')  # Hoặc redirect đến trang giỏ hàng nếu bạn muốn

def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        product.quantity = quantity
        product.total = product.price * quantity
        products.append(product)
        total_price += product.total

    return render(request, 'cart.html', {
        'products': products,
        'total_price': total_price
    })

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('trangbanhang')

    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            for _ in range(quantity):  # Nếu số lượng > 1 thì tạo nhiều Order
                Order.objects.create(
                    product=product,
                    customer_name=name,
                    customer_phone=phone,
                    customer_address=address,
                    created_at=timezone.now()
                )

        # Sau khi mua xong thì xóa giỏ hàng
        request.session['cart'] = {}

        return redirect('trangbanhang')  # Hoặc redirect ra 1 trang "Mua thành công"

    return render(request, 'checkout.html')