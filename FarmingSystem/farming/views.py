from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FarmingRecordForm
from .models import FarmingRecord


@login_required
def record_list(request):
    records = FarmingRecord.objects.filter(user=request.user).order_by('-date')
    expenses = records.filter(record_type='Expense').aggregate(total=Sum('amount'))['total'] or 0
    income = records.filter(record_type='Income').aggregate(total=Sum('amount'))['total'] or 0
    profit = income - expenses

    return render(request, 'farming/record_list.html', {
        'records': records,
        'expenses': expenses,
        'income': income,
        'profit': profit,
    })


@login_required
def record_create(request):
    if request.method == 'POST':
        form = FarmingRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            messages.success(request, 'Farming record added successfully.')
            return redirect('record_list')
        messages.error(request, 'The record could not be added. Please correct the errors below.')
    else:
        form = FarmingRecordForm()

    return render(request, 'farming/record_form.html', {
        'form': form,
        'title': 'Add Farming Record',
    })


@login_required
def record_update(request, pk):
    record = get_object_or_404(FarmingRecord, pk=pk, user=request.user)

    if request.method == 'POST':
        form = FarmingRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farming record updated successfully.')
            return redirect('record_list')
        messages.error(request, 'The record could not be updated. Please correct the errors below.')
    else:
        form = FarmingRecordForm(instance=record)

    return render(request, 'farming/record_form.html', {
        'form': form,
        'title': 'Edit Farming Record',
    })


@login_required
def record_delete(request, pk):
    record = get_object_or_404(FarmingRecord, pk=pk, user=request.user)

    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Farming record deleted successfully.')
        return redirect('record_list')

    return render(request, 'farming/record_confirm_delete.html', {
        'record': record,
    })
