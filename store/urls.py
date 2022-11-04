from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('', views.store, name="store"),
    path('user/', views.customerPage, name='user-page'),
    path('customer-setting/', views.CustomerSetting, name='customer-setting'),
    path('seller_account/', views.accountSettings, name='seller_account_setting'),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('register/', views.registerPage, name='register'),
    path('register_seller/', views.registerPageSeller, name='register_seller'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('dashboard/', views.dashboardPage, name='dashboard'),
    path('tables/', views.tablePage, name='table'),
    path('order_list/', views.orderPage, name='order_list'),

    path('addproduct/', views.addProduct, name='addproduct'),
    path('updateproduct/<str:pk>/', views.updateProduct, name='updateproduct'),
    path('deleteproduct/<str:pk>/', views.deleteProduct, name='deleteproduct'),

    path('404/', views.errorPage, name='404'),

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('category/<str:cats>/', category_list, name="cats"),
    path('store_category/<str:pk>/', store_category, name="store_category"),

    path('store_seller/<str:cats>/', views.seller_store, name="store_seller"),
    path('product_detail/<int:pk>/', views.productDetail, name="product_detail"),
    path('orderitem_list/<str:pk>/', views.Orderitems_list, name="orderitem_list"),
    path('sellertransc/', sellertransaction, name="sellertransc"),
    path('all_alerts/', all_alerts, name="all_alerts"),
    path('money_withdrawal_details/<str:pk>/', money_withdrawal_details, name="money_withdrawal_details"),
    path('user_email_change/', views.user_email_change, name="user_email_change"),
    path('searchpage_products/', views.searchpage_products, name="searchpage_products"),
    path('searchpage_store/', views.searchpage_store, name="searchpage_store"),
    path('shipping_method/', views.shipping_method, name="shipping_method"),
    path('mall_guide/', views.mall_guide, name="mall_guide"),
    path('my_webhook/', csrf_exempt(my_webhook), name="my_webhook"),

    path('reset_password/',
             auth_views.PasswordResetView.as_view(template_name='store/accounts/reset_password.html'),
             name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='store/accounts/password_reset_sent.html'),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='store/accounts/password_reset_form.html'),
         name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='store/accounts/reset_completed.html'),
         name="password_reset_complete"),

]
