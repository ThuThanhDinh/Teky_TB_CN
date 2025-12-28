# Generated manually to add payment_method field to Cart model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_useraddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='payment_method',
            field=models.CharField(choices=[('cod', 'Thanh toán khi nhận hàng'), ('bank', 'Thanh toán qua ngân hàng')], default='cod', help_text='Phương thức thanh toán', max_length=20),
        ),
    ]

