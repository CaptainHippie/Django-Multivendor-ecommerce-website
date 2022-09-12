"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #Errors page
    path('404/', views.ERROR404, name='404'),

    path('base/', views.BASE, name='base'),
    path('', views.HOME, name='home'),
    path('product/', views.PRODUCT, name='product'),
    path('product/filter-data', views.filter_data, name="filter-data"),
    path('product/<slug:slug>', views.PRODUCT_DETAILS, name='product_detail'),

    #account urls
    path('account/my-account/', views.MY_ACCOUNT, name='my_account'),
    path('account/register/', views.REGISTER, name='handleregister'),
    path('account/login/', views.LOGIN, name='handlelogin'),
    path('account/profile/', views.PROFILE, name='profile'),
    path('account/profile/update', views.PROFILE_UPDATE, name='profile_update'),
    path('account/wishlist/', views.WISHLIST, name='wishlist'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('about/', views.ABOUT, name='about'),
    path('contact/', views.CONTACT, name='contact'),
    path('faq/', views.FAQ, name='faq'),
    path('blog/', views.BLOG, name='blog'),
    path('blog-details/', views.BLOG_DETAIL, name='blog_detail'),

    #cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail,name='cart_detail'),
    path('cart/checkout/', views.CHECKOUT, name='checkout'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )

