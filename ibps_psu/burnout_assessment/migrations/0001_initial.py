# Generated by Django 4.2.6 on 2023-10-30 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BurnoutProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(blank=True, null=True, upload_to='static/img/burnout_profiles/')),
                ('profile', models.CharField(max_length=45)),
                ('description', models.TextField()),
                ('remarks', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'burnout profiles',
            },
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college_name', models.CharField(max_length=55)),
            ],
            options={
                'verbose_name_plural': 'colleges',
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_name', models.CharField(max_length=50)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='burnout_assessment.college')),
            ],
            options={
                'verbose_name_plural': 'programs',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('student_id', models.CharField(help_text='Format: ####-######-#####', max_length=20, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True)),
                ('gender', models.CharField(choices=[('Female', 'Female'), ('Male', 'Male')], max_length=6)),
                ('age', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('civil_status', models.CharField(choices=[('Single', 'Single'), ('Married', 'Married'), ('Widowed', 'Widowed'), ('Separated', 'Separated')], max_length=10)),
                ('is_profile_updated', models.BooleanField(blank=True, default=False, null=True)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='burnout_assessment.program')),
            ],
            options={
                'verbose_name_plural': 'students',
            },
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=45, null=True)),
                ('question', models.TextField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'survey questions',
            },
        ),
        migrations.CreateModel(
            name='SurveyQuestionChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=100)),
                ('value', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name_plural': 'survey question choices',
            },
        ),
        migrations.CreateModel(
            name='StudentSurveyQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='burnout_assessment.surveyquestionchoice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='burnout_assessment.surveyquestion')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='burnout_assessment.student')),
            ],
            options={
                'verbose_name_plural': 'student survey questions',
            },
        ),
        migrations.CreateModel(
            name='StudentAssessmentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('ef1_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ef2_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ef3_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ef4_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ef5_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ef6_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('cy1_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('cy2_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('cy3_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('cy4_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ex1_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ex2_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ex3_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ex4_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ex5_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ex_mean', models.FloatField(blank=True, default=None, null=True)),
                ('cy_mean', models.FloatField(blank=True, default=None, null=True)),
                ('ef_mean', models.FloatField(blank=True, default=None, null=True)),
                ('ex_high', models.BooleanField(blank=True, default=None, null=True)),
                ('cy_high', models.BooleanField(blank=True, default=None, null=True)),
                ('ef_high', models.BooleanField(blank=True, default=None, null=True)),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='burnout_assessment.burnoutprofile')),
                ('student', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='burnout_assessment.student')),
            ],
            options={
                'verbose_name_plural': 'student assessment history',
            },
        ),
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ef1_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ef2_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ef3_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ef4_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ef5_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ef6_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('cy1_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('cy2_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('cy3_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('cy4_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ex1_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ex2_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ex3_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ex4_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ex5_score', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('ex_mean', models.FloatField(blank=True, default=None, null=True)),
                ('cy_mean', models.FloatField(blank=True, default=None, null=True)),
                ('ef_mean', models.FloatField(blank=True, default=None, null=True)),
                ('ex_high', models.BooleanField(blank=True, default=None, null=True)),
                ('cy_high', models.BooleanField(blank=True, default=None, null=True)),
                ('ef_high', models.BooleanField(blank=True, default=None, null=True)),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='burnout_assessment.burnoutprofile')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='burnout_assessment.student')),
            ],
            options={
                'verbose_name_plural': 'assessment',
            },
        ),
    ]
