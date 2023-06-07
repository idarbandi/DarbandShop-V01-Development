from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("backend.apps.catalogue.urls", namespace="catalogue")),
    path("basket/", include("backend.apps.basket.urls", namespace="basket")),
    path("account/", include("backend.apps.account.urls", namespace="account")),
    path("orders/", include("backend.apps.orders.urls", namespace="orders")),
    path("checkout/", include("backend.apps.checkout.urls", namespace="checkout")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
