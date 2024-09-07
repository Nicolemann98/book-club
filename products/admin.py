from django.contrib import admin
from .models import Product, Category

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'image',
        'name',
        'author',
        'format',
        'rating',
        'price',
        'currency',
        'old_price',
        'isbn',
        'category',
        'img_paths',
    )

class CategoryAdmin(admin.ModelAdmin):
     list_display = (
        'friendly_name',
        'name',

        )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)