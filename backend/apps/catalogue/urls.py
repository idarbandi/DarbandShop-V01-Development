from . import views
from django.urls import path

app_name = "catalogue"

urlpatterns = [
    path("", views.products, name="home"),
    path("item/<slug:slug>/", views.product_detail, name="product_detail"),
    path("search/<slug:category_slug>/", views.category_list, name="category_list"),
]