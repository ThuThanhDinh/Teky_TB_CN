from django.shortcuts import render, redirect
from .models import User
from .forms import UserSignUpForm


def signUp(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Chuyển hướng sau khi đăng ký thành công
    else:
        form = UserSignUpForm()


    return render(request, 'signup-login/signup.html', {'form': form})
