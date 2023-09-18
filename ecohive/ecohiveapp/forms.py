from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Certification
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import os
from django.utils.translation import gettext_lazy as _
from datetime import datetime

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_seller','is_legaladvisor', 'is_customer','is_admin')

from django import forms
from .models import Certification  # Import the Certification model from your app

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification  # Update the model name to OrganicCertification
        fields = [
            'certification_image',
            'first_name',
            'last_name',
            'expiry_date_from',  # Remove 'expiry_date_from'
            'certification_authority',
            'phone_number',  # Add 'phone_number' field
            'certification_number',  # Add 'certification_number' field
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['certification_image'].required = False

    def clean_certification_image(self):
        certification_image = self.cleaned_data.get('certification_image')

        if certification_image:
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            file_extension = os.path.splitext(certification_image.name)[1].lower()

            if file_extension not in allowed_extensions:
                raise forms.ValidationError("Only JPG, JPEG, PNG, and GIF images are allowed.")

        return certification_image

# class CustomUserCreationForm(SignupForm):
#     # Existing fields
#     first_name = forms.CharField(max_length=30, label='First Name', required=True)
#     last_name = forms.CharField(max_length=30, label='Last Name', required=True)

#     # New fields for "Is Customer" and "Is Seller"
#     is_customer = forms.BooleanField(label='I am a Customer', required=False)
#     is_seller = forms.BooleanField(label='I am a Seller', required=False)

#     class Meta:
#         model = User  # Set to your custom user model if you're using one
#         fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_customer', 'is_seller')

#     def save(self, request):
#         # Customize the save method if necessary
#         user = super().save(request)
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.is_customer = self.cleaned_data['is_customer']
#         user.is_seller = self.cleaned_data['is_seller']
#         user.save()
#         return user

# from allauth.account.views import SignupView

# class CustomSignupView(SignupView):
#     def form_valid(self, form):
#         user = form.save(self.request)
#         user_type = self.request.POST.get('user_type')
#         # Assign the selected user type to the user
#         user.profile.user_type = user_type
#         user.profile.save()
#         return super().form_valid(form)
