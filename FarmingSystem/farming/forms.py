from django import forms

from .models import FarmingRecord


class FarmingRecordForm(forms.ModelForm):
    class Meta:
        model = FarmingRecord
        fields = ['title', 'record_type', 'amount', 'description', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
