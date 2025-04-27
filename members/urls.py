from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('members/', views.members, name='members'),
    path('home/', views.index, name='home'),
    path('register/', views.signUp, name='register'),
    path('create/', views.create, name='create'),
    path('login/', views.login, name='login'),
    path('error/', views.error, name='error'),
    path('success/', views.success, name='success'),
    path('trangchu/', views.trangchu, name='trangchu'),
    path('trangbanhang/', views.trangbanhang, name='trangbanhang'),
    path('post/', views.post, name='post'),
    path('login_success/', views.login_success, name='login_success'),
    path('san-pham/<int:product_id>/', views.product_detail, name='product_detail'),
]
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
