from django.urls import path
from . import views

urlpatterns = [
    path('',views.store,name='store'),
    path('cart/', views.cart,name='cart'),
    path('checkout',views.checkout,name='checkout'),
    path('updatecart', views.updateCart, name = 'updatecart'),
    path('updatequantity', views.updateQuantity, name = 'updatequantity'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),
]
