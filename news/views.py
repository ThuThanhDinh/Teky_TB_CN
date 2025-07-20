from django.shortcuts import render
from .models import Post
from django.views.generic import ListView

class NewsListView(ListView):
    model = Post
    template_name = 'news/home.html'
