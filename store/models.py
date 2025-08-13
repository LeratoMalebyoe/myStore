from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    """
    Represents a category for products.

    Attributes:
        name (str): The name of the category.
        slug (str): A unique slug for the category URL.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        """Return the category's name as its string representation."""
        return self.name


class Product(models.Model):
    """
    Represents a product in the store.

    Attributes:
        name (str): The name of the product.
        description (str): A detailed description of the product.
        price (Decimal): The price of the product.
        category (str): The category name (optional).
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        """Return the product's name as its string representation."""
        return self.name

    def get_absolute_url(self):
        """
        Get the absolute URL for the product detail page.

        Returns:
            str: The URL for this product's detail page.
        """
        return reverse('product_detail', args=[self.slug])


class Order(models.Model):
    """
    Represents a customer's order.

    Attributes:
        user (User): The customer who placed the order.
        created (datetime): The date and time when the order was created.
        paid (bool): Whether the order has been paid for.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        """Return a string with the order ID and username."""
        return f"Order {self.id} by {self.user.username}"

    def total(self):
        """
        Calculate the total cost of the order.

        Returns:
            Decimal: The total cost of all items in the order.
        """
        return sum(item.subtotal() for item in self.items.all())


class OrderItem(models.Model):
    """
    Represents an item within a specific order.

    Attributes:
        order (Order): The order to which this item belongs.
        product (Product): The product being ordered.
        quantity (int): The number of units ordered.
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        """
        Calculate the subtotal for this item.

        Returns:
            Decimal: The price times the quantity.
        """
        return self.product.price * self.quantity


class Profile(models.Model):
    """
    Represents additional information for a user.

    Attributes:
        user (User): The associated user account.
        bio (str): A short biography or description.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        """Return the username in the profile's string representation."""
        return f"Profile: {self.user.username}"
