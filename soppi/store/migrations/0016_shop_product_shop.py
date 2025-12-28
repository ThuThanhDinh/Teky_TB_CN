# Generated manually to add Shop model and update Product

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_cart_payment_method'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Tên cửa hàng', max_length=100)),
                ('description', models.TextField(blank=True, help_text='Mô tả cửa hàng')),
                ('logo', models.ImageField(blank=True, help_text='Logo cửa hàng', null=True, upload_to='shops/')),
                ('cover_image', models.ImageField(blank=True, help_text='Ảnh bìa cửa hàng', null=True, upload_to='shops/')),
                ('address', models.CharField(blank=True, help_text='Địa chỉ cửa hàng', max_length=200)),
                ('phone', models.CharField(blank=True, help_text='Số điện thoại', max_length=20)),
                ('is_active', models.BooleanField(default=True, help_text='Cửa hàng đang hoạt động')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(blank=True, help_text='Cửa hàng sở hữu sản phẩm', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.shop'),
        ),
    ]

