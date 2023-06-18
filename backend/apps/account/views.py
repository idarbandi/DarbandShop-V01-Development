from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterationForm, UserEditForm, UserAddressForm
from .token import account_activation_token
from .models import Customer, Address
from backend.apps.catalogue.models import Product
from backend.apps.orders.views import user_orders
from backend.apps.orders.models import Order


def account_register(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')  # account:dashboard
    if request.method == "POST":
        registerForm = RegisterationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            # Setup email
            current_site = get_current_site(request)
            subject = "Activate Your Account"
            message = render_to_string("account/registration/account_activation_email.html", {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user)
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse("Registred Successfully and Activation sent")
        else:
            return HttpResponse("Error handler Content", status=400)
    else:
        registerForm = RegisterationForm()
    return render(request, "account/registration/register.html", {"form": registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except:
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:dashboard")
    else:
        return render(request, "account/registration/activation_invalid.html")


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, "account/user/dashboard.html", {"orders": orders})
    # {"section": "profile", "orders": orders}


@login_required
def edit_detail(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()

    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, "account/user/edit_details.html", {"user_form": user_form})


@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("account:delete_confirmation")


# Addresses

@login_required
def view_addresses(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, 'account/addresses.html', {"addresses": addresses})


@login_required
def edit_addresses(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, 'account/edit_addresses.html', {"form": address_form})


@login_required
def delete_addresses(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return HttpResponseRedirect(reverse("account:addresses"))


@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user,
                           default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)

    previous_url = request.META.get('HTTP_REFERER')
    if "delivery_address" in previous_url:
        return redirect("checkout:delivery_address")

    return redirect("account:addresses")


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            userless = address_form.save(commit=False)
            userless.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
        else:
            return HttpResponse("Error handler Content", status=400)
    else:
        address_form = UserAddressForm()
    return render(request, "account/edit_addresses.html", {"form": address_form})


# Wishlist

@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, "Removed " + product.title + " From Your Wishlist")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.title + " To Your Wishlist")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, "account/user_wishlist.html", {"wishlist": products})


@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, "account/user/user_orders.html", {"orders": orders})
