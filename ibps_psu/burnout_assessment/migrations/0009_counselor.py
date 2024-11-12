# Generated by Django 4.2.6 on 2023-11-03 06:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('burnout_assessment', '0008_forgotpasswordrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counselor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('counselor_id', models.CharField(max_length=20, unique=True)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='burnout_assessment.college')),
            ],
            options={
                'verbose_name_plural': 'counselors',
            },
        ),
    ]
