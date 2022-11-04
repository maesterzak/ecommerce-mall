from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('seller','name', 'price', 'product_date', 'digital', 'category', 'image')

    def save_model(self, request, obj, form, change):
        obj.seller = request.user.seller
        super().save_model(request, obj, form, change)

    exclude = ['seller']


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'complete', 'transaction_id', 'date_orderd')
    inlines = [
        OrderItemInline,
    ]

class MoneyWithdrawlAdmin(admin.ModelAdmin):
    list_display = ('seller', 'complete', 'withdrawl_amount', 'date')


class SellertranscAdmin(admin.ModelAdmin):
    list_display = ['seller', 'ledger_balance', 'available_balance']


class TempAccountBalanceAdmin(admin.ModelAdmin):
    list_display = ['seller']


class Alert_systemAdmin(admin.ModelAdmin):
    list_display = ['alert_page','receiver_status', 'sender', 'receiver', 'date_added']

class Alert_system_customerAdmin(admin.ModelAdmin):
    list_display = ['receiver','sender_status', 'alert_page', 'date_added']


class OrderitemsStuffAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'seller', 'quantity', 'order','total']








admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingAddress)
admin.site.register(Sellertransc, SellertranscAdmin)
admin.site.register(MoneyWithdrawl, MoneyWithdrawlAdmin)
admin.site.register(TempAccountBalance, TempAccountBalanceAdmin)
admin.site.register(Alert_system, Alert_systemAdmin)
admin.site.register(Alert_system_customer, Alert_system_customerAdmin)
admin.site.register(ShipMethod)
admin.site.register(OrderitemsStuff, OrderitemsStuffAdmin)
admin.site.register(StoreType)
admin.site.register(AdminDetails)
admin.site.register(WorkerDetails)





# Register your models here.
