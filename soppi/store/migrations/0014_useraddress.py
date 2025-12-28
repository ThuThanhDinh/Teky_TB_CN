# Generated manually to add UserAddress model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_cart_voucher_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(help_text='Địa chỉ chi tiết', max_length=200)),
                ('city', models.CharField(help_text='Quận/Huyện', max_length=100)),
                ('state', models.CharField(help_text='Tỉnh/Thành phố', max_length=100)),
                ('zipcode', models.CharField(blank=True, help_text='Mã bưu điện', max_length=20, null=True)),
                ('is_default', models.BooleanField(default=False, help_text='Địa chỉ mặc định')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='store.customer')),
            ],
            options={
                'ordering': ['-is_default', '-created_at'],
            },
        ),
    ]

