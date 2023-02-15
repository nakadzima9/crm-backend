# Generated by Django 3.2.16 on 2023-02-12 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cmsapp', '0002_student_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='scheduletype',
            name='time',
            field=models.DateTimeField(null=True),
        ),
        migrations.DeleteModel(
            name='StudentCardOperation',
        ),
    ]
