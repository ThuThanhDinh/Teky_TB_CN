# members/admin.py

from django.contrib import admin
from .models import Product, post, employ, User
from .models import Order

admin.site.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

admin.site.register(post)
class postAdmin(admin.ModelAdmin):
    list_display = ('name', 'content')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

admin.site.register(employ)
class employAdmin(admin.ModelAdmin):
    list_display = ('name', 'content')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)    
admin.site.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'content')
    search_fields = ('name', 'description')
    list_filter = ('created_at',) 
# Register the Product model with custom admin interface


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer_name', 'customer_phone', 'created_at')
    search_fields = ('customer_name', 'customer_phone')
