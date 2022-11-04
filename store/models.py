from django.db import models
from django.contrib.auth.models import User
from categories.models import Category
from smartfields import fields



class WorkerDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name= models.CharField(max_length=30, blank=True)
    image = fields.ImageField(null=True, blank=True)
    phone_number = models.CharField(max_length=11, blank=True)
    whatsapp_number = models.CharField(max_length=11, blank=True)
    instagram = models.CharField(max_length=60, blank=True)
    position = models.CharField(max_length=60, blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class AdminDetails(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    phone_number=models.CharField(max_length=11, blank=True)
    whatsapp_number=models.CharField(max_length=11, blank=True)
    email=models.CharField(max_length=60, blank=True)
    facebook=models.CharField(max_length=300, blank=True)
    instagram=models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.user.__str__()

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class ShipMethod(models.Model):
    method=models.CharField(max_length=20)
    description=models.CharField(max_length=600, blank=False, default='Unknown')

    def __str__(self):
        return self.method.__str__()

class StoreType(models.Model):
    type=models.CharField(max_length=40)

    def __str__(self):
        return self.type.__str__()

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    store_name = models.CharField(max_length=25, null=True, )
    store_phone = models.CharField(max_length=11, default=0)
    store_whatsapp = models.CharField(max_length=11, default=0)
    store_type = models.ManyToManyField(StoreType, default='Uknown')
    description_store =models.TextField(max_length=300, null=True, blank=True)
    about_owner = models.TextField(max_length=300, null=True, blank=True)
    store_pic = fields.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    owner_pic=fields.ImageField(null=True, blank=True)
    shipping_method=models.ManyToManyField(ShipMethod,default='Unknown')

    def __str__(self):
        return self.user.__str__()

    @property
    def imageURL(self):
        try:
            url = self.owner_pic.url
        except:
            url = ''
        return url

    @property
    def store_imageURL(self):
        try:
            url = self.store_pic.url
        except:
            url=''
        return url


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    whatsapp_number=models.CharField(blank=True, max_length=11, null=True)
    profile_pic = fields.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.__str__()

    @property
    def imageURL(self):
        try:
            url = self.profile_pic.url
        except:
            url = ''
        return url


class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, blank=True, null=True,)
    name = models.CharField(max_length=25, null=True)
    price = models.FloatField()
    stock = models.IntegerField(default=1)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = fields.ImageField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    product_date =models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=False)
    pop_count=models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True,)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, blank=True, null=True)
    complete_seller = models.BooleanField(default=False, null=True, blank=False)
    complete_customer = models.BooleanField(default=False, null=True, blank=False)
    method=models.CharField(default='Unknown', max_length=30, blank=False)
    shipping_method = models.CharField(blank=False, default='Unknown', max_length=30)
    confirm_payment = models.BooleanField(default=False, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_order_total(self):
        orderitemsstuff = self.orderitemsstuff_set.all()
        total = sum([orderitemsstuff.total for orderitemsstuff in orderitemsstuff])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, )
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class OrderitemsStuff(models.Model):
    seller = models.CharField(max_length=200)
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    total = models.FloatField(default=0)
    digital = models.BooleanField(default=False, null=True, blank=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.id)



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, )
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Sellertransc(models.Model):
    seller=models.ForeignKey(Seller, on_delete=models.CASCADE,null=True, blank=True)
    ledger_balance = models.IntegerField(default=0, null=True, blank=True)
    available_balance = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class MoneyWithdrawl(models.Model):
    complete=models.BooleanField(default=False, null=True, blank=False)
    seller=models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    withdrawl_amount=models.IntegerField(null=True, blank=False)
    bank_account_name=models.CharField(max_length=200, null=True, blank=False)
    bank_account_number=models.IntegerField(null=True, blank=False)
    bank_name=models.CharField(max_length=200, null=True, blank=False)
    date=models.DateTimeField(auto_now_add=True, null=True,blank=False)

    def __str__(self):
        return str(self.id)


class TempAccountBalance(models.Model):
    seller=models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    ledger_balance=models.IntegerField(default=0)
    available_balance=models.IntegerField(default=0)
    withdrawl=models.ForeignKey(MoneyWithdrawl, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return str(self.id)


class Alert_system(models.Model):
    receiver_status=models.CharField(default='unknown', blank=False, max_length=40)
    sender=models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=False)
    receiver=models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=False)
    alert_text=models.CharField(max_length=300, blank=False, default='There is no message here')
    date_added=models.DateTimeField(auto_now=True)
    alert_page=models.CharField(max_length=30, default='uknown')
    order=models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    money_withdrawal=models.ForeignKey(MoneyWithdrawl, on_delete=models.SET_NULL, null=True, blank=False)

    def __str__(self):
        return str(self.id)


class Alert_system_customer(models.Model):
    sender_status=models.CharField(default='Uknown', blank=False, max_length=40)
    alert_text=models.CharField(max_length=300, blank=False, default='Uknown')
    date_added=models.DateTimeField(auto_now_add=True)
    receiver=models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=False)
    alert_page=models.CharField(max_length=30, default='Uknown')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)



# Create your models here.
