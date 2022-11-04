from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *
from django.forms.widgets import CheckboxSelectMultiple



class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields=['complete_seller', 'complete_customer']

class SellerForm(ModelForm):
    class Meta:
        model = Seller
        fields = '__all__'
        exclude =['user',]

    def __init__(self, *args, **kwargs):
        super(SellerForm, self).__init__(*args, **kwargs)
        self.fields["shipping_method"].widget =CheckboxSelectMultiple()
        self.fields["shipping_method"].queryset = ShipMethod.objects.all()
        self.fields["store_type"].widget = CheckboxSelectMultiple()
        self.fields["store_type"].queryset = StoreType.objects.all()

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude =['user',]



class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['seller', 'pop_count']

    def save_model(self, request, obj, form, change):
        obj.seller = request.user.seller
        super().save_model(request, obj, form, change)


class CreateUserForm(UserCreationForm):
    class Meta:
        model =User
        fields = {'username', 'email','password1', 'password2'}
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat Password'

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(
            username=username).count():
            raise forms.ValidationError('This email is already in use! Try another email')
        return email


class MoneyWithrawalForm(ModelForm):
    class Meta:
        model=MoneyWithdrawl
        fields = '__all__'
        exclude = ['seller', 'complete']


class User_Form(ModelForm):
    class Meta:
        model=User
        fields=['email']


