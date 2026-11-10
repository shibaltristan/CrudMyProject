from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render


def login_view(request):
    if request.user.is_authenticated:
        return redirect('record_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.GET.get('next') or 'record_list')
        messages.error(request, 'Login failed. Check your Farmers ID and password.')
    else:
        form = AuthenticationForm(request)

    form.fields['username'].label = 'Farmers ID'
    return render(request, 'registration/login.html', {'form': form})
