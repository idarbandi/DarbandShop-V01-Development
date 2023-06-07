from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)

from .models import Address, Customer


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control mb-3",
               "placeholder": "Username", "id": "login-username"}
    ))
    password = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Password",
            "id": "login-pwd"
        }

    ))


class RegisterationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_name"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Username"})
        self.fields["email"].widget.attrs.update(
            {"class": "form-control mb-3 w-75", "placeholder": "E-mail", "name": "email", "id": "email"})
        self.fields["password"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Password"})
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Repeat Password"})

    user_name = forms.CharField(
        label="Enter User Name", min_length=4, max_length=50, help_text="Required", widget=forms.TextInput)
    email = forms.EmailField(max_length=100, help_text="Required", error_messages={
        "Required": "Oops Please Provide an Email Address"})
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password Again", widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ("user_name", "email",)

    def clean_user_name(self):
        user_name = self.cleaned_data["user_name"].lower()
        r = Customer.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("user name already Exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passwords do not match")
        return cd['password']

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("Entered Email Has Already been Taken")
        return email


class UserEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True

    email = forms.EmailField(
        label="Accounts Email (Can Not Be Changed)", max_length=200, widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "email",
                   "id": "form-email", "readonly": "readonly"},
        )
    )

    first_name = forms.CharField(
        label="first_name", min_length=4, max_length=50, widget=forms.TextInput(
            attrs={"class": "form-control mb-3",
                   "placeholder": "Firstname", "id": "form-firstname"}
        )
    )

    class Meta:
        model = Customer
        fields = ("email", "first_name")


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={"class": "form-control mb-3", "placeholder": "Email", "id": "form-email"}
    ))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                "Unfortunatly We Can Not Find The Entered Email Address")
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password", widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": "New Password", "id": "form-newpass"}))
    new_password2 = forms.CharField(
        label="Repeat Password", widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": "New Password", "id": "form-new-pass2"}))


# Address
class UserAddressForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields['phone'].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Phone"}
        )
        self.fields['address_line'].widget.attrs.update(
            {"class": "form-control mb-2 account-form"}
        )
        self.fields['address_line_2'].widget.attrs.update(
            {"class": "form-control mb-2 account-form"}
        )
        self.fields['town_city'].widget.attrs.update(
            {"class": "form-control mb-2 account-form"}
        )
        self.fields['post_code'].widget.attrs.update(
            {"class": "form-control mb-2 account-form"}
        )

    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'post_code', 'address_line', 'address_line_2', 'town_city']
