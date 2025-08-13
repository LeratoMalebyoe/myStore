from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderItem, Profile
from .forms import SignUpForm, CartAddForm, CheckoutForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Simple session-based cart using product ids
CART_SESSION_ID = 'cart'


def _get_cart(request):
    """
    Retrieve the current shopping cart from the session.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: The cart dictionary stored in the session.
    """
    return request.session.setdefault(CART_SESSION_ID, {})


def _save_cart(request, cart):
    """
    Save the updated cart to the session and mark it as modified.

    Args:
        request (HttpRequest): The HTTP request object.
        cart (dict): The cart data to be saved.
    """
    request.session[CART_SESSION_ID] = cart
    request.session.modified = True


def home(request):
    """
    Render the store homepage showing all products.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered homepage with product listings.
    """
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


def product_list(request):
    """
    Display a list of all available products.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered product list page.
    """
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, slug):
    """
    Display details for a single product and handle cart addition.

    If the request is POST, the product is added to the session cart.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The unique slug identifying the product.

    Returns:
        HttpResponse: Rendered product detail page.
    """
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
    """
    Add a product to the session cart or increment its quantity.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to add.

    Returns:
        HttpResponseRedirect: Redirect to the cart view.
    """
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
    """
    Display the current cart contents with totals.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered cart page with items and total price.
    """
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
    """
    Process the checkout and create an order from the cart.

    If POST, creates an Order and associated OrderItems, then clears the cart.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered checkout confirmation or checkout form.
    """
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
    """
    Handle user signup and create a related profile.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered signup form or redirect after successful signup.
    """
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
    """
    Display the logged-in user's profile page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered profile page for the current user.
    """
    profile = request.user.profile
    return render(request, 'store/profile.html', {'profile': profile})
