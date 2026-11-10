from django.contrib import admin

from .models import FarmingRecord


@admin.register(FarmingRecord)
class FarmingRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'record_type', 'amount', 'date', 'user')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(user=request.user)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
