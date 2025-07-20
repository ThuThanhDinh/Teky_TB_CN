from django.urls import path, include
from .views import NewsListView
urlpatterns = [
    path('', NewsListView.as_view(), name='home'),
    path('ff/',NewsListView.as_view(),name ='post_detail'),
    path('fff/', NewsListView.as_view(), name='post_new'),
    path('fffff/', NewsListView.as_view(), name='post_edit'),
    path('ffffff/',NewsListView.as_view(), name='post_delete'),
    path('fffffff/',NewsListView.as_view(), name='comment_new'),
    
]