# Generated by Django 5.0.1 on 2024-02-24 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('burnout_assessment', '0017_alter_student_contact_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='BurnoutFactor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factor', models.CharField(max_length=50)),
                ('count', models.IntegerField(default=None)),
            ],
            options={
                'verbose_name_plural': 'burnout factors',
            },
        ),
    ]
