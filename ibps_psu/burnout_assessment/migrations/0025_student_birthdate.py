# Generated by Django 5.0.1 on 2024-04-16 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('burnout_assessment', '0024_college_is_assessment_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='birthdate',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
