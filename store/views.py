from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderItem, Profile
from .forms import SignUpForm, CartAddForm, CheckoutForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Simple session-based cart using product ids
CART_SESSION_ID = 'cart'

def _get_cart(request):
    return request.session.setdefault(CART_SESSION_ID, {})

def _save_cart(request, cart):
    request.session[CART_SESSION_ID] = cart
    request.session.modified = True

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = CartAddForm()
    if request.method == 'POST':
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart = _get_cart(request)
            pid = str(product.id)
            qty = form.cleaned_data['quantity']
            cart[pid] = cart.get(pid, 0) + qty
            _save_cart(request, cart)
            return redirect('cart')
    return render(request, 'store/product_detail.html', {'product': product, 'form': form})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1  # increment nested quantity
    else:
        cart[product_id_str] = {
        'name': product.name,
        'price': str(product.price),
        'quantity': 1,
    }
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('store:cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    total = 0
    items = []

    for product_id, item in cart.items():
        if isinstance(item, dict):
            price = float(item.get('price', 0))
            quantity = item.get('quantity', 0)
            subtotal = price * quantity
            total += subtotal
            item['subtotal'] = subtotal
            items.append(item)
        else:
            # Handle or skip invalid cart entries
            continue

    return render(request, 'store/cart.html', {'items': items, 'total': total})

@login_required
def checkout(request):
    cart = _get_cart(request)
    if not cart:
        return redirect('store:product_list')
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, created=timezone.now(), paid=False)
        for pid, item in cart.items():
            p = Product.objects.get(id=pid)
            # if item is dict
            quantity = item['quantity'] if isinstance(item, dict) else item
            OrderItem.objects.create(order=order, product=p, quantity=quantity)
        request.session[CART_SESSION_ID] = {}
        return render(request, 'store/checkout.html', {'order': order})
    return render(request, 'store/checkout.html')



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'store/signup.html', {'form': form})

@login_required
def profile(request):
    profile = request.user.profile
    return render(request, 'store/profile.html', {'profile': profile})