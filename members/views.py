from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Product, post
from .forms import UserSignUpForm
from django.shortcuts import render, redirect


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

def trangbanhang(request):
  template = loader.get_template('trangbanhang.html')
  productdata = Product.objects.all()
  return HttpResponse(template.render())

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