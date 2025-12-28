# Generated manually to add voucher fields to Cart model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_rank_voucher'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='voucher_code',
            field=models.CharField(blank=True, help_text='Voucher code applied to this order', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='subtotal',
            field=models.FloatField(default=0, help_text='Subtotal before discount and shipping'),
        ),
        migrations.AddField(
            model_name='cart',
            name='discount_amount',
            field=models.FloatField(default=0, help_text='Discount amount from voucher'),
        ),
        migrations.AddField(
            model_name='cart',
            name='shipping',
            field=models.FloatField(default=0, help_text='Shipping cost'),
        ),
        migrations.AddField(
            model_name='cart',
            name='final_total',
            field=models.FloatField(default=0, help_text='Final total after discount and shipping'),
        ),
    ]

