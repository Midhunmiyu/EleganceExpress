from django.shortcuts import redirect, render
from django.views import View
from store.models import Cart, Customer, OrderPlaced, Product
from .forms import CustomerRegistrationForm, CustomerProfileForm, OrderForm, ProductForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def home(request):
    Mobile = Product.objects.filter(category='M')
    Laptop = Product.objects.filter(category='L')
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(User=request.user))
    return render(request, 'app/home.html', {'Mobile': Mobile, 'Laptop': Laptop, 'totalitem': totalitem})


@login_required(login_url='login')
def admindashboard(request):
    return render(request, 'app/adminbase.html')


@login_required(login_url='login')
def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request,"Product added succeesfully...!!")
            return redirect('view_product')
    return render(request, 'app/addproducts.html', {'form': form})


@login_required(login_url='login')
def view_product(request):
    product = Product.objects.all()
    return render(request, 'app/viewproduct.html', {'product': product})


@login_required(login_url='login')
def delete(request, id):
    data = Product.objects.get(id=id)
    data.delete()
    return redirect('view_product')


@login_required(login_url='login')
def order_view(request):
    order = OrderPlaced.objects.all()
    return render(request, 'app/order_view.html', {'order': order})


@login_required(login_url='login')
def order_delete(request, id):
    data = OrderPlaced.objects.get(id=id)
    data.delete()
    return redirect('order_view')


@login_required(login_url='login')
def order_update(request, id):
    data = OrderPlaced.objects.get(id=id)
    form = OrderForm(instance=data)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('order_view')
    return render(request, 'app/update_order.html', {'form': form})


def product_detail(request, pk):
    totalitem = 0
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(User=request.user))
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(User=request.user)).exists()
    return render(request, 'app/productdetail.html',
                  {'product': product, 'item_already_in_cart': item_already_in_cart, 'totalitem': totalitem})


@login_required(login_url='login')
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(User=user, product=product).save()
    return redirect('/cart')


@login_required(login_url='login')
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        user = request.user
        totalitem = len(Cart.objects.filter(User=request.user))
        cart = Cart.objects.filter(User=user)
        amount = 0.0
        shipping_amount = 70.0
        temp_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.User == user]
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount
                total_amount = shipping_amount + amount
            return render(request, 'app/addtocart.html',
                          {'carts': cart, 'amount': amount, 'total_amount': total_amount, 'totalitem': totalitem})
        else:
            return render(request, 'app/emptycart.html')


@login_required(login_url='login')
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(User=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        temp_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.User == request.user]

        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': shipping_amount + amount
        }
        return JsonResponse(data)


@login_required(login_url='login')
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(User=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        temp_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.User == request.user]

        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': shipping_amount + amount
        }
        return JsonResponse(data)


@login_required(login_url='login')
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(User=request.user))

        c.delete()

        amount = 0.0
        shipping_amount = 70.0
        temp_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.User == request.user]

        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount

        data = {

            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)


@login_required(login_url='login')
def buy_now(request):
    return render(request, 'app/buynow.html')


@login_required(login_url='login')
def profile(request):
    form = CustomerProfileForm()
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(User=request.user))
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']
            reg = Customer(User=usr, name=name, locality=locality, city=city, state=state, pincode=pincode)
            reg.save()

            messages.success(request, 'Profile Updated Successfully...!!')
            return redirect('profile')
    return render(request, 'app/profile.html', {'form': form, 'totalitem': totalitem})


@login_required(login_url='login')
def address(request):
    data = Customer.objects.filter(User=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(User=request.user))
    return render(request, 'app/address.html', {'data': data, 'totalitem': totalitem})


@login_required(login_url='login')
def orders(request):
    op = OrderPlaced.objects.filter(User=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})


@login_required(login_url='login')
def change_password(request):
    return render(request, 'app/changepassword.html')


def mobile(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(User=request.user))
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'redmi' or data == 'samsung' or data == 'oneplus':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    return render(request, 'app/mobile.html', {'mobiles': mobiles, 'totalitem': totalitem})


def laptop(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(User=request.user))
    if data == None:
        laptop = Product.objects.filter(category='L')
    elif data == 'lenovo' or data == 'hp':
        laptop = Product.objects.filter(category='L').filter(brand=data)
    return render(request, 'app/laptop.html', {'laptop': laptop, 'totalitem': totalitem})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                auth_login(request, user)
                return redirect('admindashboard')

            else:
                auth_login(request, user)
                return redirect('profile')
        else:
            messages.info(request, 'invalid Credentials')
    return render(request, 'app/login.html')


class CustomerRegistartionView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations..!! Registration Successful..!!')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


@login_required(login_url='login')
def checkout(request):
    user = request.user
    add = Customer.objects.filter(User=user)
    cart_items = Cart.objects.filter(User=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0

    cart_product = [p for p in Cart.objects.all() if p.User == request.user]
    if cart_product:
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
        total_amount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add': add, 'total_amount': total_amount, 'item': cart_items})


@login_required(login_url='login')
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(User=user)
    for c in cart:
        OrderPlaced(User=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    messages.success(request,"Order placed successfully..!!")
    return redirect('orders')


def logout_view(request):
    logout(request)
    return redirect('home')
