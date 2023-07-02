from django.contrib import admin

from store.models import Customer, Cart, OrderPlaced,  Product


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'User', 'name', 'locality', 'city', 'state', 'pincode']


@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'User', 'customer', 'product', 'quantity', 'ordered_date', 'status']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category',
                    'product_image']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'User', 'product', 'quantity']


