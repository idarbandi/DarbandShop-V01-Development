from django.shortcuts import render
from .models import Category, Product
from django.shortcuts import get_object_or_404, render


def categories(request):
    return {
        "categories": Category.objects.all()
    }


def all_products(request):
    products = Product.objects.all()
    return render(request, "store/home.html", {"products": products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, "store/products/detail.html", {"product": product})


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = Product.objects.filter(category=category)
    return render(request, "store/products/category.html", {"category": category, "products": product})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request, "store/products/detail.html", {"product": category})
