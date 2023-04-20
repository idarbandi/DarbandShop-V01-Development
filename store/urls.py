from . import views
from django.urls import path

app_name = "store"

urlpatterns = [
    path("", views.all_products, name="all_products"),
    path("item/<slug:slug>/", views.product_detail, name="product_detail"),
    path("search/<slug:category_slug>/", views.category_list, name="category_list"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
]