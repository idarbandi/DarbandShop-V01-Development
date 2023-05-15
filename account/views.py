from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .forms import RegisterationForm, UserEditForm
from .token import account_activation_token
from .models import UserBase
from orders.views import user_orders

def account_register(request):
    # if request.user.is_authenticated:
    #     return reverse("/")  # account:dashboard
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
        registerForm = RegisterationForm()
    return render(request, "account/registration/register.html", {"form": registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
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
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("account:delete_confirmation")

