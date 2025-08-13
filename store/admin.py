from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Profile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model, prepopulates slug from name."""
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model, displays name, price, and category."""
    list_display = ('name','price','category')
    list_filter = ('category',)

class OrderItemInline(admin.TabularInline):
    """Inline display of OrderItem within Order admin."""
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for Order model, includes OrderItem inline."""
    list_display = ('id','user','created','paid')
    inlines = [OrderItemInline]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for Profile model, displays user."""
    list_display = ('user',)
