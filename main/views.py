from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, CartItem, Purchase
from .forms import ProductForm
from django.contrib.auth.forms import UserCreationForm

# -----------------------------
# Authentication Views
# -----------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')  # already logged in → go to feed

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', '')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(next_url or 'feed')
        else:
            messages.error(request, 'Invalid username or password.')

    next_url = request.GET.get('next', '')
    return render(request, 'main/login.html', {'next': next_url})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('feed')  # prevent re-signup

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after signup
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('feed')
        else:
            messages.error(request, 'Signup failed. Please correct the errors.')
    else:
        form = UserCreationForm()

    return render(request, 'main/signup.html', {'form': form})


# -----------------------------
# Product Views
# -----------------------------
@login_required(login_url='login')
def feed_view(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'main/feed.html', {'products': products})


@login_required(login_url='login')
def add_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, '✅ Product added successfully!')
            return redirect('feed')
    else:
        form = ProductForm()
    return render(request, 'main/add_product.html', {'form': form})


@login_required(login_url='login')
def my_listings(request):
    products = Product.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'main/my_listings.html', {'products': products})


@login_required(login_url='login')
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'main/product_detail.html', {'product': product})


# -----------------------------
# Dashboard
# -----------------------------
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'main/dashboard.html')


# -----------------------------
# Cart Views
# -----------------------------
@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'🛒 {product.title} added to cart!')
    return redirect('cart')


@login_required(login_url='login')
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'main/cart.html', {'cart_items': cart_items, 'total': total})


@login_required(login_url='login')
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.info(request, '❌ Item removed from cart.')
    return redirect('cart')


@login_required(login_url='login')
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    for item in cart_items:
        Purchase.objects.create(user=request.user, product=item.product, quantity=item.quantity)
        item.delete()

    messages.success(request, '✅ Checkout complete! Thank you for your purchase.')
    return redirect('purchases')


# -----------------------------
# Purchase History
# -----------------------------
@login_required(login_url='login')
def view_purchases(request):
    purchases = Purchase.objects.filter(user=request.user).order_by('-purchased_at')
    return render(request, 'main/previous_purchases.html', {'purchases': purchases})
