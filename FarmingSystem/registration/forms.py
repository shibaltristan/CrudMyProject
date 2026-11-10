from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import FarmerRegistration


class FarmerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Create a secure password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password'}))

    class Meta:
        model = FarmerRegistration
        fields = ['farmers_id', 'first_name', 'last_name', 'middle_name', 'mobile_number']
        widgets = {
            'farmers_id': forms.TextInput(attrs={'placeholder': 'Example: FARM-001'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'middle_name': forms.TextInput(attrs={'placeholder': 'Optional middle name'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': '09XXXXXXXXX', 'inputmode': 'tel'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['middle_name'].required = False

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        elif password:
            try:
                validate_password(password)
            except ValidationError as error:
                self.add_error('password', error)

        farmers_id = cleaned_data.get('farmers_id')
        if farmers_id and User.objects.filter(username=farmers_id).exists():
            self.add_error('farmers_id', 'A farmer with this Farmers ID already exists.')

        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        registration = super().save(commit=False)
        user = User.objects.create_user(
            username=registration.farmers_id,
            password=self.cleaned_data['password'],
            first_name=registration.first_name,
            last_name=registration.last_name,
        )
        registration.user = user
        if commit:
            registration.save()
        return registration
