from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def remove_unowned_records(apps, schema_editor):
    FarmingRecord = apps.get_model('farming', 'FarmingRecord')
    FarmingRecord.objects.filter(user__isnull=True).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('farming', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='farmingrecord',
            name='user',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='farming_records',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(remove_unowned_records, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='farmingrecord',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='farming_records',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
