from django.contrib import admin
from .models import Customer, Product, Cart, Cartitems, ShippingAddress, Rank, Voucher, Shop, UserAddress

# --- Hàm tạo ModelAdmin tự động hiển thị mọi field ---
def all_fields_admin(model):
    class AutoAdmin(admin.ModelAdmin):
        list_display = [field.name for field in model._meta.fields]
    return AutoAdmin

# --- Đăng ký tất cả model với admin ---
admin.site.register(Customer, all_fields_admin(Customer))
admin.site.register(Product, all_fields_admin(Product))
admin.site.register(Cart, all_fields_admin(Cart))
admin.site.register(Cartitems, all_fields_admin(Cartitems))
admin.site.register(ShippingAddress, all_fields_admin(ShippingAddress))
admin.site.register(Rank, all_fields_admin(Rank))
admin.site.register(Voucher, all_fields_admin(Voucher))
admin.site.register(Shop, all_fields_admin(Shop))
admin.site.register(UserAddress, all_fields_admin(UserAddress))
