# Generated by Django 3.0.8 on 2022-04-20 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smartfields.fields
import smartfields.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0004_auto_20200517_1832'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=11, null=True)),
                ('whatsapp_number', models.CharField(blank=True, max_length=11, null=True)),
                ('profile_pic', smartfields.fields.ImageField(blank=True, null=True, upload_to='')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=(smartfields.models.SmartfieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MoneyWithdrawl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complete', models.BooleanField(default=False, null=True)),
                ('withdrawl_amount', models.IntegerField(null=True)),
                ('bank_account_name', models.CharField(max_length=200, null=True)),
                ('bank_account_number', models.IntegerField(null=True)),
                ('bank_name', models.CharField(max_length=200, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_orderd', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False, null=True)),
                ('transaction_id', models.CharField(max_length=200, null=True)),
                ('complete_seller', models.BooleanField(default=False, null=True)),
                ('complete_customer', models.BooleanField(default=False, null=True)),
                ('method', models.CharField(default='Unknown', max_length=30)),
                ('shipping_method', models.CharField(default='Unknown', max_length=30)),
                ('confirm_payment', models.BooleanField(default=False, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=25, null=True)),
                ('store_phone', models.CharField(default=0, max_length=11)),
                ('store_whatsapp', models.CharField(default=0, max_length=11)),
                ('description_store', models.TextField(blank=True, max_length=300, null=True)),
                ('about_owner', models.TextField(blank=True, max_length=300, null=True)),
                ('store_pic', smartfields.fields.ImageField(blank=True, null=True, upload_to='')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('owner_pic', smartfields.fields.ImageField(blank=True, null=True, upload_to='')),
            ],
            bases=(smartfields.models.SmartfieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ShipMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=20)),
                ('description', models.CharField(default='Unknown', max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='StoreType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='WorkerDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('image', smartfields.fields.ImageField(blank=True, null=True, upload_to='')),
                ('phone_number', models.CharField(blank=True, max_length=11)),
                ('whatsapp_number', models.CharField(blank=True, max_length=11)),
                ('instagram', models.CharField(blank=True, max_length=60)),
                ('position', models.CharField(blank=True, max_length=60)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=(smartfields.models.SmartfieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TempAccountBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ledger_balance', models.IntegerField(default=0)),
                ('available_balance', models.IntegerField(default=0)),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Seller')),
                ('withdrawl', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.MoneyWithdrawl')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=200, null=True)),
                ('state', models.CharField(max_length=200, null=True)),
                ('zipcode', models.CharField(max_length=200, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Customer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Sellertransc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ledger_balance', models.IntegerField(blank=True, default=0, null=True)),
                ('available_balance', models.IntegerField(blank=True, default=0, null=True)),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Seller')),
            ],
        ),
        migrations.AddField(
            model_name='seller',
            name='shipping_method',
            field=models.ManyToManyField(default='Unknown', to='store.ShipMethod'),
        ),
        migrations.AddField(
            model_name='seller',
            name='store_type',
            field=models.ManyToManyField(default='Uknown', to='store.StoreType'),
        ),
        migrations.AddField(
            model_name='seller',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, null=True)),
                ('price', models.FloatField()),
                ('stock', models.IntegerField(default=1)),
                ('digital', models.BooleanField(default=False, null=True)),
                ('image', smartfields.fields.ImageField(blank=True, null=True, upload_to='')),
                ('Description', models.TextField(blank=True, null=True)),
                ('product_date', models.DateTimeField(auto_now_add=True)),
                ('pop_count', models.IntegerField(default=0)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='categories.Category')),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Seller')),
            ],
            bases=(smartfields.models.SmartfieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OrderitemsStuff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200, null=True)),
                ('price', models.FloatField()),
                ('total', models.FloatField(default=0)),
                ('digital', models.BooleanField(default=False, null=True)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Seller'),
        ),
        migrations.AddField(
            model_name='moneywithdrawl',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Seller'),
        ),
        migrations.CreateModel(
            name='Alert_system_customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_status', models.CharField(default='Uknown', max_length=40)),
                ('alert_text', models.CharField(default='Uknown', max_length=300)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('alert_page', models.CharField(default='Uknown', max_length=30)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Order')),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Alert_system',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver_status', models.CharField(default='unknown', max_length=40)),
                ('alert_text', models.CharField(default='There is no message here', max_length=300)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('alert_page', models.CharField(default='uknown', max_length=30)),
                ('money_withdrawal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.MoneyWithdrawl')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Order')),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Seller')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='AdminDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=11)),
                ('whatsapp_number', models.CharField(blank=True, max_length=11)),
                ('email', models.CharField(blank=True, max_length=60)),
                ('facebook', models.CharField(blank=True, max_length=300)),
                ('instagram', models.CharField(blank=True, max_length=300)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
