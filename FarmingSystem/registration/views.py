from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .forms import FarmerRegistrationForm


def register(request):
    if request.user.is_authenticated:
        return redirect('record_list')

    if request.method == 'POST':
        form = FarmerRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save()
            user = authenticate(
                request,
                username=registration.farmers_id,
                password=form.cleaned_data['password'],
            )
            if user:
                login(request, user)
                messages.success(request, 'Your farmer account was created successfully.')
                return redirect('record_list')
        else:
            messages.error(request, 'Your account could not be created. Please correct the errors below.')
    else:
        form = FarmerRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
