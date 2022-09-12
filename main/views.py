from django.shortcuts import render, redirect
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Max, Min

from cart.cart import Cart

# Create your views here.
def BASE(request):
    return render(request, 'base.html')

def HOME(request):
    sliders = Slider.objects.all().order_by('-id')[0:3]
    banners = Banner.objects.all().order_by('-id')[0:3]

    main_category = Main_Category.objects.all().order_by('-id')[0:8]
    product = Product.objects.all().filter(section__name = 'Limited time deal')
    
    context = {
            'sliders': sliders,
            'banners': banners,
            'main_category': main_category,
            'products': product
    }
    return render(request, 'main/home.html', context)

def PRODUCT_DETAILS(request, slug):
    product = Product.objects.filter(slug = slug)
    if product.exists():
        product = Product.objects.get(slug = slug)
    else:
        return redirect('404')
    
    context = {
        'product': product,
    }
    return render(request, 'product/product_detail.html', context)

def ERROR404(request):
    return render(request, 'errors/404.html')

def MY_ACCOUNT(request):
    return render(request, 'account/my_account.html')

def REGISTER(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username = username).exists():
            messages.error(request,"username already exists")
            return redirect('login')
        if User.objects.filter(email = email).exists():
            messages.error(request,"email already exists")
            return redirect('login')
        
        user = User(
            username = username,
            email = email
        )
        user.set_password(password)
        user.save()
        return redirect('login')

def LOGIN(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username = username).exists():
            user_auth = authenticate(request, username=username, password=password)
            if user_auth is not None:
                login(request, user_auth)
                return redirect('home')
            else:
                messages.error(request, 'Invalid password!')
                return redirect('login')
        else:
            messages.error(request, 'username not found!')
            return redirect('login')

@login_required(login_url='/accounts/login/')
def PROFILE(request):
    return render(request, 'profile/profile.html')

@login_required(login_url='/accounts/login/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id
        
        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request, 'Profile successfully updated!')
        return redirect('profile')
        
def ABOUT(request):
    return render(request, 'main/about.html')

def CONTACT(request):
    return render(request, 'main/contact.html')

def FAQ(request):
    return render(request, 'main/faq.html')

def BLOG(request):
    return render(request, 'main/blog.html')

def BLOG_DETAIL(request):
    return render(request, 'main/blog_details.html')

def PRODUCT(request):
    category =Category.objects.all()
    product = Product.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()
    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))

    FilterPrice = request.GET.get('FilterPrice')
    Int_FilterPrice = FilterPrice and int(FilterPrice)
    ColorID = request.GET.get('ColorID')
    if FilterPrice and ColorID:
        product = Product.objects.filter(price__lte = Int_FilterPrice, color = ColorID)
    elif FilterPrice:
        product = Product.objects.filter(price__lte = Int_FilterPrice)
    elif ColorID:
        product = Product.objects.filter(color = ColorID)
    else:
        product = Product.objects.all()

    context = {
        'category': category,
        'product': product,
        'brand': brand,
        'min_price': min_price,
        'max_price': max_price,
		'FilterPrice': FilterPrice,
        'color': color
    }
    return render(request, 'product/product.html', context)

def WISHLIST(request):
    return render(request, 'profile/wishlist.html')

def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    product_num = request.GET.getlist('product_num[]')

    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(categories__id__in=categories).distinct()

    if len(product_num) > 0:
        allProducts = allProducts.all().order_by('-id')[0:1]

    if len(brands) > 0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()

    t = render_to_string('ajax/product.html', {'product': allProducts})

    return JsonResponse({'data': t})



@login_required(login_url="/accounts/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_detail(request):
    cart = request.session.get('cart')
    packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    total_tax = 0
    for i in cart.values():
        if i:
            total_tax = total_tax + ( i['tax'] * i['price'] * i['quantity'] / 100)
    
    valid_coupon = None
    coupon = None
    invalid_coupon = None
    if request.method == "GET":
        coupon_code = request.GET.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon_Code.objects.get(code = coupon_code)
                valid_coupon = "Applicable on current order!"
            except:
                invalid_coupon = "Invalid coupon!"
    context = {
	    'packing_cost': packing_cost,
        'total_tax': total_tax,
        'coupon': coupon,
        'valid_coupon': valid_coupon,
        'invalid_coupon': invalid_coupon
        }

    return render(request, 'cart/cart.html', context)


def CHECKOUT(request):
    return render(request, 'cart/checkout.html')







