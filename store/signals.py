from django.db.models.signals import post_save, pre_save
from .models import *
from django.dispatch import receiver


# sellertransactions signals
@receiver(pre_save, sender=Order)
def sellertransc_updated(sender, instance, **kwargs):
    try:
        order = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        if not order.complete == instance.complete:
            sellertransc = Sellertransc.objects.filter(seller=order.seller)
            ledger = Sellertransc.objects.get(seller=order.seller)
            sellertransc.update(ledger_balance=(ledger.ledger_balance + order.get_cart_total))


@receiver(pre_save, sender=Order)
def available_balance_updated(sender, instance, **kwargs):
    try:
        order = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        if instance.complete_customer is True and instance.complete_seller is True:
            sellertransc = Sellertransc.objects.filter(seller=order.seller)
            available = Sellertransc.objects.get(seller=order.seller)
            sellertransc.update(available_balance=(available.available_balance + order.get_order_total))


# temp account balance
@receiver(post_save, sender=MoneyWithdrawl)
def tempaccountbalance_create(sender, instance, created, **kwargs):
    if created:
        sellertrasnc = Sellertransc.objects.get(seller=instance.seller)
        TempAccountBalance.objects.create(ledger_balance=sellertrasnc.ledger_balance,
                                          seller=sellertrasnc.seller,
                                          available_balance=sellertrasnc.available_balance,
                                          withdrawl=instance)
        tempaccount_update = TempAccountBalance.objects.filter(seller=instance.seller)
        tempaccount_update.update(ledger_balance=(sellertrasnc.ledger_balance - instance.withdrawl_amount),
                                  available_balance=(sellertrasnc.available_balance - instance.withdrawl_amount))


@receiver(post_save, sender=MoneyWithdrawl)
def withdrawl_update(sender, instance, created, **kwargs):
    if not created:
        if instance.complete is True:
            sellertrasnc_update = Sellertransc.objects.filter(seller=instance.seller)
            sellertransc = Sellertransc.objects.get(seller=instance.seller)
            sellertrasnc_update.update(ledger_balance=(sellertransc.ledger_balance - instance.withdrawl_amount),
                                       available_balance=(sellertransc.available_balance - instance.withdrawl_amount))
            tempaccount = TempAccountBalance.objects.get(seller=instance.seller)
            tempaccount.delete()


# product stock
@receiver(post_save, sender=Order)
def orderitem_update(sender, instance, created, **kwargs):
    if created is False:
        if not instance.complete:
            orderitems = OrderItem.objects.filter(order=instance)
            for orderitem in orderitems:
                prod = Product.objects.filter(name=orderitem.product.name)
                product = Product.objects.get(name=orderitem.product.name)
                prod.update(stock=(product.stock - orderitem.quantity))


# Alert system
@receiver(pre_save, sender=Order)
def alert_system_order_update(sender, instance, **kwargs):
    if instance.complete:
        try:
            alert = Alert_system.objects.get(sender=instance.customer, order=instance)

        except Alert_system.DoesNotExist:
            if instance.method == 'Whatsapp':
                alert_system, created = Alert_system.objects.update_or_create(sender=instance.customer, order=instance,
                                                                              receiver=instance.seller,
                                                                              receiver_status='New',
                                                                              alert_text='A new order has been made to your store with payment method[Whatsapp] by ' + instance.customer.name,
                                                                              alert_page='Order_Alert')

                alert_system.save()
            elif instance.method == 'Flutterwave':
                alert_system, created = Alert_system.objects.update_or_create(sender=instance.customer, order=instance,
                                                                              receiver=instance.seller,
                                                                              receiver_status='New',
                                                                              alert_text='A new order has been made to your store with payment method[Flutterwave] by ' + instance.customer.name,
                                                                              alert_page='Order_Alert')

                alert_system.save()
        else:
            if alert:
                pass


@receiver(post_save, sender=MoneyWithdrawl)
def alert_system_withdrawl_update(sender, instance, created, **kwargs):
    if created:
        alert_system = Alert_system.objects.create(
            receiver=instance.seller, receiver_status='New',
            alert_text='Your Money Withdrawal action has been initialized,transaction shall be completed within 24hrs',
            alert_page='Money_withdrawal', money_withdrawal=instance)

        alert_system.save()
    elif not created:
        if instance.complete:
            alert_system = Alert_system.objects.create(
                receiver=instance.seller, receiver_status='New',
                alert_text='Withdrawal Transaction successful,The following amount has been transferred  into your account, AMOUNT= ₦' + str(
                    instance.withdrawl_amount),
                alert_page='Money_withdrawal_complete', money_withdrawal=instance)

            alert_system.save()


# Alert system for customers
@receiver(pre_save, sender=Order)
def alert_system_customer_order_update(sender, instance, **kwargs):
    if instance.complete:
        try:
            alert = Alert_system_customer.objects.get(receiver=instance.customer, order=instance)

        except Alert_system_customer.DoesNotExist:
            if instance.method == 'Whatsapp':
                alert_system_customer, created = Alert_system_customer.objects.update_or_create(
                    receiver=instance.customer, order=instance,
                    sender_status='New',
                    alert_text='Your new order has been initialized with payment method[Whatsapp] please ensure to contact the seller to complete payment, Seller: ' + instance.seller.store_name,
                    alert_page='Order_Alert')

                alert_system_customer.save()
            elif instance.method == 'Flutterwave':
                alert_system_customer, created = Alert_system_customer.objects.update_or_create(
                    receiver=instance.customer, order=instance,
                    sender_status='New',
                    alert_text='Your new order has been initialized with payment method[Flutterwave] to Seller: ' + instance.seller.store_name,
                    alert_page='Order_Alert')

                alert_system_customer.save()

        else:
            if alert:
                pass


@receiver(pre_save, sender=Order)
def orderitems_list_update(sender, instance, **kwargs):
    if instance.complete == True:
        orderitemsstuff=OrderitemsStuff.objects.filter(order=instance)
        if orderitemsstuff:
            pass
        else:
            orderitems = OrderItem.objects.filter(order=instance)
            for orderitem in orderitems:
                orderitemsstuff = OrderitemsStuff.objects.create(seller=instance.seller.store_name, order=instance,
                                                                 digital=orderitem.product.digital,
                                                                 name=orderitem.product.name,
                                                                 price=orderitem.product.price,
                                                                 quantity=orderitem.quantity, total=orderitem.get_total
                                                                 )

                orderitemsstuff.save()

