from django.contrib import admin

from .models import FarmerProfile


@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('farmers_id', 'first_name', 'middle_name', 'last_name', 'mobile_number', 'user')
    search_fields = ('farmers_id', 'first_name', 'last_name', 'mobile_number')
