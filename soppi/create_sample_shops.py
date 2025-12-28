#!/usr/bin/env python
"""
Script để tạo shop mẫu cho hệ thống
Chạy: python manage.py shell < create_sample_shops.py
Hoặc: python manage.py shell
>>> exec(open('create_sample_shops.py').read())
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soppi.settings')
django.setup()

from store.models import Shop

# Tạo các shop mẫu
shops_data = [
    {
        'name': 'Nhà Hàng Gà Rán KFC',
        'description': 'Thương hiệu gà rán nổi tiếng thế giới với hương vị đặc trưng',
        'address': '123 Đường Nguyễn Huệ, Quận 1, TP.HCM',
        'phone': '1900 1234',
        'is_active': True,
    },
    {
        'name': 'Pizza Hut',
        'description': 'Pizza ngon, nóng hổi, đa dạng topping',
        'address': '456 Đường Lê Lợi, Quận 1, TP.HCM',
        'phone': '1900 5678',
        'is_active': True,
    },
    {
        'name': 'Bánh Mì Sài Gòn',
        'description': 'Bánh mì truyền thống Sài Gòn với nhiều loại nhân',
        'address': '789 Đường Điện Biên Phủ, Quận Bình Thạnh, TP.HCM',
        'phone': '0901 234 567',
        'is_active': True,
    },
    {
        'name': 'Cơm Tấm Cali',
        'description': 'Cơm tấm đặc sản miền Nam với sườn nướng thơm lừng',
        'address': '321 Đường Võ Văn Tần, Quận 3, TP.HCM',
        'phone': '0902 345 678',
        'is_active': True,
    },
    {
        'name': 'Trà Sữa Gong Cha',
        'description': 'Trà sữa Đài Loan chính hiệu, nhiều topping',
        'address': '654 Đường Nguyễn Trãi, Quận 5, TP.HCM',
        'phone': '0903 456 789',
        'is_active': True,
    },
]

created_count = 0
for shop_data in shops_data:
    shop, created = Shop.objects.get_or_create(
        name=shop_data['name'],
        defaults=shop_data
    )
    if created:
        created_count += 1
        print(f"✓ Đã tạo shop: {shop.name}")
    else:
        print(f"- Shop đã tồn tại: {shop.name}")

print(f"\nTổng cộng: {created_count} shop mới được tạo")
print(f"Tổng số shop trong hệ thống: {Shop.objects.filter(is_active=True).count()}")

