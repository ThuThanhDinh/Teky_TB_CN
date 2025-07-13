from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'users/home.html')

def dangnhap(request):
    return render(request, 'dangnhap/dangnhap.html')

def dangky(request):
    return render(request, 'dangky/dangky.html')
