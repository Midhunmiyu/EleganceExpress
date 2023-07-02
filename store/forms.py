from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from store.models import Customer, OrderPlaced, Product

class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    email = forms.CharField(required=True,label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','state','pincode']
        labels = {'name':'Name','locality':'Locality','city':'City','pincode0':'Pincode','state':'State'}
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),'locality':forms.TextInput(attrs={'class':'form-control'}),'city':forms.TextInput(attrs={'class':'form-control'}),'state':forms.Select(attrs={'class':'form-control'}),'pincode':forms.NumberInput(attrs={'class':'form-control'})}


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderPlaced
        fields = '__all__'
        widgets = {'User':forms.TextInput( attrs={'readonly': 'readonly','class':'form-control'}),'customer':forms.TextInput(attrs={'readonly': 'readonly','class':'form-control'}),'product':forms.TextInput(attrs={'readonly': 'readonly','class':'form-control'}),'quantity':forms.NumberInput(attrs={'readonly': 'readonly','class':'form-control'}),'ordered_date':forms.DateInput(attrs={'readonly': 'readonly','class':'form-control'})}