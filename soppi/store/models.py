from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.lookups import IntegerFieldFloatRounding
# Create your models here.
class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)

    email = models.EmailField()

class Shop(models.Model):
    """Cửa hàng/Shop giống Shopee Food"""
    name = models.CharField(max_length=100, help_text='Tên cửa hàng')
    description = models.TextField(blank=True, help_text='Mô tả cửa hàng')
    logo = models.ImageField(upload_to='shops/', null=True, blank=True, help_text='Logo cửa hàng')
    cover_image = models.ImageField(upload_to='shops/', null=True, blank=True, help_text='Ảnh bìa cửa hàng')
    address = models.CharField(max_length=200, blank=True, help_text='Địa chỉ cửa hàng')
    phone = models.CharField(max_length=20, blank=True, help_text='Số điện thoại')
    is_active = models.BooleanField(default=True, help_text='Cửa hàng đang hoạt động')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def average_rating(self):
        """Tính rating trung bình từ các sản phẩm"""
        from django.db.models import Avg
        products = self.products.all()
        if products.exists():
            ratings = []
            for product in products:
                avg = product.comments.aggregate(Avg('rating'))['rating__avg']
                if avg:
                    ratings.append(avg)
            if ratings:
                return sum(ratings) / len(ratings)
        return 0
    
    @property
    def product_count(self):
        """Số lượng sản phẩm"""
        return self.products.count()
    
    def __str__(self):
        return self.name


class Product(models.Model):

    name =  models.CharField(max_length=50)

    price = models.FloatField(default=10.55)
    description = models.TextField(null=True, blank=True)

    image = models.ImageField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products', null=True, blank=True, help_text='Cửa hàng sở hữu sản phẩm')


class Cart(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    cart_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Voucher and pricing information
    voucher_code = models.CharField(max_length=50, null=True, blank=True, help_text='Voucher code applied to this order')
    subtotal = models.FloatField(default=0, help_text='Subtotal before discount and shipping')
    discount_amount = models.FloatField(default=0, help_text='Discount amount from voucher')
    shipping = models.FloatField(default=0, help_text='Shipping cost')
    final_total = models.FloatField(default=0, help_text='Final total after discount and shipping')
    payment_method = models.CharField(max_length=20, choices=[('cod', 'Thanh toán khi nhận hàng'), ('bank', 'Thanh toán qua ngân hàng')], default='cod', help_text='Phương thức thanh toán')


    @property

    def get_cart_total(self):

        cartitems = self.cartitems_set.all()

        total = sum([item.get_total for item in cartitems])

        return total

   

    @property

    def get_itemtotal(self):

        cartitems = self.cartitems_set.all()

        total = sum([item.quantity for item in cartitems])

        return total


    def __str__(self):

        return str(self.id)


class Cartitems(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    product =  models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=0)


    @property

    def get_total(self):

        total = self.quantity * self.product.price

        if total == 0.00:

            self.delete()

        return total


   


    def __str__(self):

        return self.product.name


class ShippingAddress(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    address = models.CharField(max_length=100)

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    zipcode = models.CharField(max_length=100)


class UserAddress(models.Model):
    """Địa chỉ giao hàng được lưu của user"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(max_length=200, help_text='Địa chỉ chi tiết')
    city = models.CharField(max_length=100, help_text='Quận/Huyện')
    state = models.CharField(max_length=100, help_text='Tỉnh/Thành phố')
    zipcode = models.CharField(max_length=20, blank=True, null=True, help_text='Mã bưu điện')
    is_default = models.BooleanField(default=False, help_text='Địa chỉ mặc định')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}"


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}⭐)"


class Rank(models.Model):
    name = models.CharField(max_length=30, unique=True)
    threshold = models.BigIntegerField(default=0)

    def __str__(self):
        return f"{self.name} (≥ {self.threshold})"


class Voucher(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percent = models.IntegerField(default=0, help_text='Discount percent (0 if fixed amount)')
    max_amount = models.FloatField(null=True, blank=True, help_text='Maximum discount amount')
    min_purchase = models.FloatField(default=0, help_text='Minimum cart subtotal to use voucher')
    fixed_amount = models.FloatField(null=True, blank=True, help_text='Fixed discount amount (use instead of percent when set)')
    ranks = models.ManyToManyField(Rank, blank=True, related_name='vouchers')
    image = models.ImageField(upload_to='vouchers/', null=True, blank=True)
    free_shipping = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)
    desc = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} ({'enabled' if self.enabled else 'disabled'})"