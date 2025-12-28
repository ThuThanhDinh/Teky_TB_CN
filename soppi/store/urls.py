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
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('shop/<int:shop_id>/', views.shop_detail, name='shop_detail'),
    path('purchase-history/', views.purchase_history, name='purchase_history'),
    path('vouchers/', views.vouchers_list, name='vouchers'),
    path('voucher/<str:voucher_code>/', views.voucher_detail, name='voucher_detail'),
    path('profile/', views.profile, name='profile'),
    path('profile/address/add/', views.add_address, name='add_address'),
    path('profile/address/<int:address_id>/edit/', views.edit_address, name='edit_address'),
    path('profile/address/<int:address_id>/delete/', views.delete_address, name='delete_address'),
    path('profile/address/<int:address_id>/set-default/', views.set_default_address, name='set_default_address'),
]

