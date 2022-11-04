from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
import json
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import *
from categories.models import Category
from .forms import *
from .decorators import unauthenticated_user, allowed_users
import sweetify
from .filters import ProductFilter


@login_required(login_url='login')
@allowed_users(allowed_roles=['sellers', 'Admin'])
def sellertransaction(request):
    admin_details = AdminDetails.objects.all()
    seller=request.user.seller
    sellertransc=Sellertransc.objects.get(seller=seller)
    form = MoneyWithrawalForm()
    if request.method == 'POST':
        form = MoneyWithrawalForm(request.POST)
        if form.is_valid():
            try:
                temp=TempAccountBalance.objects.get(seller=seller)
                if temp:
                    sweetify.info(request, 'You cannot make a withdrawal, wait until pending one is completed by Admin',
                                   button='Ok', timer=50000)
            except TempAccountBalance.DoesNotExist:

                obj = form.save(commit=False)
                obj.seller = request.user.seller
                if obj.withdrawl_amount < sellertransc.available_balance:
                    sweetify.info(request, 'Done', button='ok')
                    obj.save()
                    form=MoneyWithrawalForm()
                else:
                    sweetify.info(request, 'The amount you requested exceeds amount in Available balance',
                                   button='Ok', timer=50000)
    context = {'sellertransc':sellertransc, 'form':form, 'admin_details':admin_details}
    return render(request, 'store/accounts/sellertransc.html', context)


def category_list(request, cats):
    admin_details = AdminDetails.objects.all()
    if request.user.is_authenticated:
        if request.user.groups.filter(name='customer').exists():
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            sweetify.info(request,
                          'User is not a customer, meaning your either a mall naija worker or a seller, create a customer account to be able to purchase products',
                           button='Ok', timer=50000)
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
            cartItems = order['get_cart_items']
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    post_by_category = Product.objects.filter(category=cats).order_by('-product_date')
    category = Category.objects.get(id=cats)
    page = request.GET.get('page', 1)
    paginator = Paginator(post_by_category, 3)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {'page_obj':page_obj,'cartItems': cartItems, 'category':category, 'admin_details':admin_details}
    return render(request,'store/category_list.html', context)


# Create your views here.

def store(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='customer').exists():
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            sweetify.info(request,
                          'User is not a customer, meaning your either a mall naija worker or a seller, create a customer account to be able to purchase products',
                           button='Ok', timer=50000)
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
            cartItems = order['get_cart_items']
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    worker_details=WorkerDetails.objects.all
    admin_details=AdminDetails.objects.all()
    products = Product.objects.all().order_by('-pop_count')[:3]
    category_list = Category.objects.all().exclude(parent=5).exclude(name='Blog')
    store_category=StoreType.objects.all()

    store_list = Seller.objects.all().exclude(store_name=None).order_by('date_created')

    page = request.GET.get('page', 1)
    paginator = Paginator(store_list, 9)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {'cartItems': cartItems, 'products': products,
               'category_list':category_list, 'page_obj':page_obj,
               'store_category':store_category, 'admin_details':admin_details, 'worker_details':worker_details}
    return render(request, 'store/store.html', context)


@login_required(login_url='login')
def cart(request):
    pro_digital = False
    shipping_meths=False
    admin_details = AdminDetails.objects.all()
    if request.user.is_authenticated:
        if request.user.groups.filter(name='customer').exists():
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items

            for orderitem in items:
                if orderitem.product.digital == False:
                    shipping_meths = True
                    pro_digital = False
                    break
                elif orderitem.product.digital == True:
                    pro_digital = True
            if pro_digital:
                ordd = Order.objects.filter(customer=customer, id=order.id)
                ordd.update(shipping_method='No Shipping')


        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
            cartItems = order['get_cart_items']

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    context = {'items':items, 'order':order, 'cartItems':cartItems, 'shipping_meths':shipping_meths, 'admin_details':admin_details}
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def shipping_method(request):
    shipping_M=None
    admin_details = AdminDetails.objects.all()
    if request.user.is_authenticated:
        if request.user.groups.filter(name='customer').exists():
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
            ordeitems = OrderItem.objects.filter(order=order)
            if order.seller:
                shipping_M=order.seller.shipping_method.all()
            else:
                shipping_M=None
            oll = Order.objects.filter(id=order.id)
            if request.method == 'POST':
                oldd = request.POST.get('order')
                chng= request.POST.get('chng_btn')
                if oldd:
                    oll.update(shipping_method=oldd)
                    if order.shipping_method != 'Unknown':
                        sweetify.info(request, 'method updated')
                elif chng:
                    oll.update(shipping_method='Unknown')

            if order.shipping_method != 'Unknown':
                sweetify.info(request, 'method updated')
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
            cartItems = order['get_cart_items']
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context={'shipping_M':shipping_M, 'order':order, 'cartItems': cartItems, 'items':items, 'admin_details':admin_details}
    return render(request, 'store/shipping_method.html', context)


@login_required(login_url='login')
def checkout(request):
    stock=None
    quantity=None
    product=None
    confirm = True
    shipping_meths=False
    pro_digital=False
    public_key = "FLWPUBK_TEST-e58205b76cd53d9f469a266f8d4a6ba6-X"
    admin_details = AdminDetails.objects.all()
    if request.user.is_authenticated:
        if request.user.groups.filter(name='customer').exists():
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
            ordeitems = OrderItem.objects.filter(order=order)

            for orderitem in items:
                if orderitem.product.digital ==False:
                    shipping_meths=True
                    pro_digital=False
                    break
                elif orderitem.product.digital ==True:
                    pro_digital=True
            if pro_digital:
                ordd=Order.objects.filter(customer=customer, id=order.id)
                ordd.update(shipping_method='No Shipping')

            for orderitem in ordeitems:
                if orderitem.product.stock < orderitem.quantity:
                    sweetify.info(request, 'one of your cart items is out of stock', button='ok')
                    confirm = False
                    product=orderitem.product
                    stock=orderitem.product.stock
                    quantity=orderitem.quantity
                    break
                else:
                    confirm = True

            confirm = confirm
            if request.method == 'POST':
                dan = request.POST.get('info')
                if dan:
                    ode = Order.objects.filter(customer=customer, id=order.id)
                    ode.update(method='Whatsapp')
                mal= request.POST.get('info2')
                if mal:
                    od = Order.objects.filter(customer=customer, id=order.id)
                    od.update(method='Flutterwave')

        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
            cartItems = order['get_cart_items']
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    name = datetime.datetime.now().strftime('%H:%M:%S')
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'name': name, 'confirm': confirm, 'product': product,'quantity': quantity, 'stock': stock, 'shipping_meths':shipping_meths, 'public_key':public_key, 'admin_details':admin_details}
    return render(request, 'store/checkout.html', context)


@allowed_users(allowed_roles=['customer'])
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    seller= Seller.objects.get(product=productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created= Order.objects.get_or_create(complete=False, customer=customer)
    items=order.orderitem_set.all()
    if items:
        if seller ==order.seller:
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

            if action == 'add':
                if orderItem.quantity < product.stock:
                    orderItem.quantity = (orderItem.quantity + 1)
                    sweetify.info(request, 'item added', button='Ok')
                else:
                    sweetify.info(request, 'reached maximum amount of available stock')
            elif action == 'remove':
                sweetify.info(request, 'item removed', button='ok')
                orderItem.quantity = (orderItem.quantity - 1)


            orderItem.save()

            if orderItem.quantity <= 0:
                orderItem.delete()
            if order.get_cart_items <=0:
                ordss=Order.objects.filter(id=order.id)
                ordss.update(shipping_method='Unknown', seller=None, method='Unknown')

        else:
            sweetify.info(request, 'Cannot add items from 2 different stores into one cart', button='Ok', timer=50000)

    else:
        order, created = Order.objects.update_or_create(customer=customer, complete=False, defaults={'seller':seller})
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        if action == 'add':
            if orderItem.quantity < product.stock:
                orderItem.quantity = (orderItem.quantity + 1)
                sweetify.info(request, 'item added',button='Ok')
            else:
                sweetify.info(request, 'sorry product is out of stock')
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)


        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@allowed_users(allowed_roles=['customer'])
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form'] ['total'])
        order.transaction_id=transaction_id

        if total== order.get_cart_total:
            order.complete = True
            order.save()
            orderitems_count = OrderItem.objects.filter(order=order)
            for orderitem in orderitems_count:
                orderitem.product.pop_count = (orderitem.product.pop_count + 1)
                orderitem.product.save()

        if order.shipping==True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping'] ['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    else:
        print('user is not logged in...')

    return JsonResponse('Payment complete!', safe=False)


@unauthenticated_user
def registerPage(request):
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user=form.save()
                username = form.cleaned_data.get('username')
                group = Group.objects.get(name='customer')
                user.groups.add(group)
                Customer.objects.create(
                    user=user,
                )
                messages.success(request, 'Account was created for '+ username)
                return redirect('login')

        context={'form':form}
        return render(request, 'store/accounts/register.html', context)


@unauthenticated_user
def registerPageSeller(request):
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user=form.save()
                username = form.cleaned_data.get('username')
                group = Group.objects.get(name='sellers')
                user.groups.add(group)
                Seller.objects.create(
                    user=user
                )
                Sellertransc.objects.create(
                    ledger_balance='0',
                    seller=user.seller,
                    available_balance='0'
                )
                messages.success(request, 'Sellers Account was created for '+ username)
                return redirect('login')

        context={'form':form}
        return render(request, 'store/accounts/register2.html', context)


@unauthenticated_user
def loginPage(request):
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.groups.filter(name='customer').exists():
                    login(request, user)
                    if user.customer.name:
                        return redirect('store')
                    else:
                        return redirect('customer-setting')
                elif user.groups.filter(name='sellers').exists():
                    login(request, user)
                    if user.seller.store_name:
                        return redirect('dashboard')
                    else:
                        return redirect('seller_account_setting')
                elif user.groups.filter(name='admin').exists():
                    login(request, user)
                    return redirect('admin:index')
                else:
                    login(request, user)
                    return redirect('cart')
            else:
                messages.info(request, 'Username OR Password is incorrect')

        context={}
        return render(request, 'store/accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'sellers'])
def dashboardPage(request):
    global alert_page_obj
    alert_count = None
    products = request.user.seller.product_set.all()
    orders = request.user.seller.order_set.all()
    seller=request.user.seller
    order_total=Order.objects.filter(seller=seller, complete=True).count()
    product_all=products.count()
    if request.user.groups.filter(name='sellers').exists():
        sellertransaction=Sellertransc.objects.get(seller=seller)
        alert_order=Alert_system.objects.filter(receiver=seller).order_by('-date_added')
        alert_count=Alert_system.objects.filter(receiver=seller, receiver_status='New').count()
        alert_page = request.GET.get('page', 1)
        alert_paginator = Paginator(alert_order, 4)
        try:
            alert_page_obj = alert_paginator.page(alert_page)
        except PageNotAnInteger:
            alert_page_obj = alert_paginator.page(1)
        except EmptyPage:
            alert_page_obj = alert_paginator.page(alert_paginator.num_pages)

    context={'sellertransaction':sellertransaction,'alert_count':alert_count, 'alert_page_obj':alert_page_obj,'products':products, 'orders':orders, 'seller':seller, 'order_total':order_total, 'product_all':product_all}
    return render(request, 'store/accounts/dashboard.html', context)


def errorPage(request):
    context={}
    return render(request, 'store/accounts/404.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def customerPage(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer, complete=True)
    alert_order = Alert_system_customer.objects.filter(receiver=customer).order_by('-date_added')
    alert_count = Alert_system_customer.objects.filter(receiver=customer, sender_status='New').count()
    alert_page = request.GET.get('page', 1)
    alert_paginator = Paginator(alert_order, 4)
    try:
        alert_page_obj = alert_paginator.page(alert_page)
    except PageNotAnInteger:
        alert_page_obj = alert_paginator.page(1)
    except EmptyPage:
        alert_page_obj = alert_paginator.page(alert_paginator.num_pages)

    context = {'customer': customer,'orders': orders, 'alert_page_obj':alert_page_obj, 'alert_count':alert_count}
    return render(request, 'store/accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'sellers'])
def tablePage(request):
    seller=request.user.seller
    products = request.user.seller.product_set.all()
    orders = request.user.seller.order_set.all()
    alert_order = Alert_system.objects.filter(receiver=seller).order_by('-date_added')
    alert_count = Alert_system.objects.filter(receiver=seller, receiver_status='New').count()
    alert_page = request.GET.get('page', 1)
    alert_paginator = Paginator(alert_order, 4)
    try:
        alert_page_obj = alert_paginator.page(alert_page)
    except PageNotAnInteger:
        alert_page_obj = alert_paginator.page(1)
    except EmptyPage:
        alert_page_obj = alert_paginator.page(alert_paginator.num_pages)

    context={'products':products, 'orders':orders,'alert_page_obj':alert_page_obj, 'alert_count':alert_count}
    return render(request, 'store/accounts/tables.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'sellers'])
def addProduct(request):
    admin_details = AdminDetails.objects.all()
    form = ProductForm
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.seller=request.user.seller
            obj.save()
            return redirect('/tables')
    context ={'form':form, 'admin_details':admin_details}
    return render(request, 'store/accounts/add_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'sellers'])
def updateProduct(request, pk):
    admin_details = AdminDetails.objects.all()
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product, )
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/tables')
    context = {'form':form, 'admin_details':admin_details}
    return render(request, 'store/accounts/add_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'sellers'])
def deleteProduct(request, pk):
    admin_details = AdminDetails.objects.all()
    product = Product.objects.get(id=pk)
    if request.method=='POST':
        product.delete()
        return redirect('/tables')
    context = {'product':product, 'admin_details':admin_details}

    return render(request, 'store/accounts/delete_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sellers'])
def accountSettings(request):
    admin_details = AdminDetails.objects.all()
    user = request.user
    seller = request.user.seller
    form = SellerForm(instance=seller)

    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES ,instance=seller)
        if form.is_valid():
            if seller.store_name:
                store_name = Seller.objects.filter(store_name=seller.store_name).exclude(id=seller.id).exists()
                if store_name:
                    sweetify.info(request, 'Store name is already taken try another')
                else:
                    sweetify.info(request, 'Details Updated')
                    form.save()
            else:
                print('no store name')
                store_name = Seller.objects.filter(store_name=seller.store_name).exists()
                if store_name:
                    sweetify.info(request, 'Store name is already taken try another')
                else:
                    sweetify.info(request, 'Details Updated')
                    form.save()

    context = {'form':form, 'user':user, 'admin_details':admin_details}
    return render(request, 'store/accounts/seller_account_setting.html', context)


def seller_store(request, cats):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='customer').exists():
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            sweetify.info(request,
                          'user is not a customer, meaning your either a mall naija worker or a seller, create a customer account to ')
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
            cartItems = order['get_cart_items']
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    seller_products = Product.objects.filter(seller=cats).order_by('-product_date')
    seller_detail = Seller.objects.filter(id=cats)
    myFilter= ProductFilter(request.GET, queryset=seller_products)
    seller_products=myFilter.qs
    page = request.GET.get('page', 1)
    paginator = Paginator(seller_products, 10)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {'page_obj': page_obj, 'cartItems': cartItems, 'cats':cats, 'seller_detail':seller_detail, 'myFilter':myFilter,}
    return render(request,'store/accounts/seller_store.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'sellers'])
def orderPage(request):
    seller = request.user.seller
    products = Product.objects.filter(seller=seller)
    orderitems = OrderItem.objects.filter(product__in=products)
    orders = Order.objects.filter(seller=seller, complete=True)
    alert_order = Alert_system.objects.filter(receiver=seller).order_by('-date_added')
    alert_count = Alert_system.objects.filter(receiver=seller, receiver_status='New').count()
    alert_page = request.GET.get('page', 1)
    alert_paginator = Paginator(alert_order, 4)
    try:
        alert_page_obj = alert_paginator.page(alert_page)
    except PageNotAnInteger:
        alert_page_obj = alert_paginator.page(1)
    except EmptyPage:
        alert_page_obj = alert_paginator.page(alert_paginator.num_pages)

    context = {'seller': seller, 'orderitems': orderitems, 'orders': orders, 'alert_page_obj':alert_page_obj,'alert_count':alert_count}
    return render(request, 'store/accounts/orders.html', context)


def productDetail(request, pk):
    admin_details = AdminDetails.objects.all()
    if request.user.is_authenticated:
        if request.user.groups.filter(name='customer').exists():
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            sweetify.info(request,
                          'user is not a customer, meaning your either a mall naija worker or a seller, create a customer account to ')
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
            cartItems = order['get_cart_items']
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    product=Product.objects.get(id=pk)
    print('product:',product)
    context={'product':product, 'cartItems':cartItems, 'admin_details':admin_details}
    return render(request, 'store/product_detail.html', context)


@login_required(login_url='login')
def Orderitems_list(request, pk):
    global ship
    status = False
    admin_details = AdminDetails.objects.all()

    if request.user.groups.filter(name='sellers').exists() :
        seller=request.user.seller
        order=Order.objects.get(seller=seller, id=pk)
        if order.complete_seller == True and order.complete_customer == True:
            sweetify.info(request, 'ORDER DONE')
            status = True
        else:
            status = False
            shipping=False
        if request.method=='POST':
            ans = request.POST.get('alert_btn')
            alert_system = Alert_system.objects.filter(receiver=seller, order=order)
            if ans:
                if alert_system:
                    alert_system.update(receiver_status='Old')



    elif request.user.groups.filter(name='customer').exists():
        customer=request.user.customer
        order=Order.objects.get(customer=customer, complete=True, id=pk)
        if order.complete_seller == True and order.complete_customer == True:
            sweetify.info(request, 'ORDER DONE')
            status = True
        else:
            status = False
        if request.method=='POST':
            ans = request.POST.get('alert_btn')
            alert_system_customer = Alert_system_customer.objects.filter(receiver=customer, order=order)
            if ans:
                if alert_system_customer:

                    alert_system_customer.update(sender_status='Old')
    else:
        sweetify.error(request, 'your not allowed on this page')
    form = OrderForm(instance=order,)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()


    orderitems = OrderitemsStuff.objects.filter(order=pk)
    shipped=ShippingAddress.objects.filter(order=pk)
    if shipped:
        ship=ShippingAddress.objects.get(order=pk)
        shipping=True
    else:
        ship=None
        shipping=False
    context = {'orderitems': orderitems, 'pk': pk, 'form': form, 'order': order, 'status': status, 'shipping':shipping,'ship':ship, 'admin_details':admin_details}
    return render(request, 'store/accounts/orderitems.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def CustomerSetting(request):
    admin_details = AdminDetails.objects.all()
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES ,instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form, 'admin_details':admin_details}
    return render(request, 'store/accounts/user-setting.html', context)

@login_required(login_url='login')
def all_alerts(request):
    admin_details = AdminDetails.objects.all()
    if request.user.groups.filter(name='sellers').exists():
        seller=request.user.seller
        alert=Alert_system.objects.filter(receiver=seller).order_by('-date_added')
    elif request.user.groups.filter(name='customer').exists() :
        customer=request.user.customer
        alert=Alert_system_customer.objects.filter(receiver=customer).order_by('-date_added')


    else:
        sweetify.info(request, 'You have no business here')

    context={'alert':alert, 'admin_details':admin_details}
    return render(request, 'store/accounts/all_alerts.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'sellers'])
def money_withdrawal_details(request, pk):
    admin_details = AdminDetails.objects.all()
    seller=request.user.seller
    money_withdrawal=MoneyWithdrawl.objects.filter(seller=seller, id=pk)
    if request.method == 'POST':
        ans = request.POST.get('alert_btn')
        alert_system= Alert_system.objects.filter(receiver=seller, money_withdrawal=pk)
        if ans:
            if alert_system:
                alert_system.update(receiver_status='Old')
    context={'money_withdrawal':money_withdrawal, 'admin_details':admin_details}
    return render(request, 'store/accounts/money_withdrawal_details.html', context)


def user_email_change(request):
    admin_details = AdminDetails.objects.all()
    user=request.user
    user_form = User_Form(instance=user)

    if request.method == 'POST':
        user_form =User_Form(request.POST, instance=user)
        if user_form.is_valid():
            user_exist = User.objects.filter(email=user.email).exists()
            if user_exist:
                print('user exists')
                sweetify.info(request, 'EMAIL ALREADY EXISTS')
            else:
                print('user does not exist')
                sweetify.info(request, 'EMAIL HAS BEEN UPDATED')
                user_form.save()

    context = {'user_form': user_form, 'admin_details':admin_details}
    return render(request, 'store/accounts/change_email.html', context)


def searchpage_products(request):
    admin_details = AdminDetails.objects.all()
    if request.user.is_authenticated:
        if request.user.groups.filter(name='customer').exists():
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            sweetify.info(request,
                          'user is not a customer, meaning your either a mall naija worker or a seller, create a customer account to ')
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
            cartItems = order['get_cart_items']
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)

    context={'products':products, 'query':query, 'order':order, 'cartItems':cartItems, 'admin_details':admin_details}
    return render(request, 'store/accounts/searchpage_products.html', context)


def searchpage_store(request):
    admin_details = AdminDetails.objects.all()
    if request.user.is_authenticated:
        if request.user.groups.filter(name='customer').exists():
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            sweetify.info(request,
                          'user is not a customer, meaning your either a mall naija worker or a seller, create a customer account to ')
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
            cartItems = order['get_cart_items']
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    query = request.GET.get('q')

    if query:
        store = Seller.objects.filter(store_name__icontains=query)

    context={'store':store, 'query':query, 'order':order, 'cartItems':cartItems, 'admin_details':admin_details}
    return render(request, 'store/accounts/searchpage_store.html', context)


def store_category(request, pk):
    admin_details = AdminDetails.objects.all()
    if request.user.is_authenticated:
        if request.user.groups.filter(name='customer').exists():
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            sweetify.info(request,
                          'User is not a customer, meaning your either a mall naija worker or a seller, create a customer account to be able to purchase products',
                           button='Ok', timer=50000)
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
            cartItems = order['get_cart_items']
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    store_typ=StoreType.objects.get(id=pk)
    stores=Seller.objects.filter(store_type=pk)

    page = request.GET.get('page', 1)
    paginator = Paginator(stores, 2)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context={'stores':stores, 'store_typ':store_typ, 'cartItems':cartItems, 'page_obj':page_obj, 'admin_details':admin_details}
    return render(request, 'store/store_category.html', context)


def mall_guide(request):

    context={}
    return render(request, 'store/mall_guide.html')


@require_POST
@csrf_exempt
def my_webhook(request):
    jsondata = request.body
    data = json.loads(jsondata)
    jsoddata1 = request.headers
    data1 = jsoddata1['Verif-Hash']
    status= data['status']
    amount = data['amount']
    id=data['txRef']
    if data1 == '45fds@466!799':
        if status == 'successful':
            ord=Order.objects.get(id=id)

            if ord.get_cart_total == amount:
                order=Order.objects.filter(id=id)
                if order:
                    order.update(confirm_payment=True)

    return HttpResponse(status=200)


