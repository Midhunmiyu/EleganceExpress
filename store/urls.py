from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from store import views

urlpatterns = [
    path('', views.home,name='home'),
    path('product-detail/<int:pk>/', views.product_detail, name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/',auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',success_url= '/passwordchangedone/'),name='changepassword'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>/', views.mobile, name='mobiledata'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>/', views.laptop, name='laptopdata'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('registration/', views.CustomerRegistartionView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),

    path('paymentdone/', views.payment_done, name='paymentdone'),

    #  admin urls

    path('admindashboard/', views.admindashboard,name='admindashboard'),
    path('add_product/', views.add_product,name='add_product'),
    path('view_product/', views.view_product,name='view_product'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('order_view/', views.order_view,name='order_view'),
    path('order_delete/<int:id>/', views.order_delete, name='order_delete'),
    path('order_update/<int:id>/', views.order_update, name='order_update'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
