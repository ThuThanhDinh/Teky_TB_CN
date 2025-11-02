from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:item_id>/', views.increase_cartitem, name='increase_cartitem'),
    path('cart/decrease/<int:item_id>/', views.decrease_cartitem, name='decrease_cartitem'),
    path('cart/reset/', views.reset_cart_quantities, name='reset_cart_quantities'),
    path('cart/remove/<int:item_id>/', views.remove_cartitem, name='remove_cartitem'),
]

