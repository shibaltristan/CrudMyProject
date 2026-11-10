from django.conf import settings
from django.db import models


class FarmingRecord(models.Model):
    RECORD_TYPES = [
        ('Expense', 'Expense'),
        ('Income', 'Income'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='farming_records',
    )
    title = models.CharField(max_length=100)
    record_type = models.CharField(max_length=20, choices=RECORD_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField()

    def __str__(self):
        return self.title
