from django.contrib import admin

from .models import FarmerRegistration


@admin.register(FarmerRegistration)
class FarmerRegistrationAdmin(admin.ModelAdmin):
    list_display = ('farmers_id', 'first_name', 'middle_name', 'last_name', 'mobile_number', 'user')
    search_fields = ('farmers_id', 'first_name', 'last_name', 'mobile_number')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(user=request.user)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
