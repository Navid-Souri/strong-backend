# Generated by Django 5.2.3 on 2025-07-03 13:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workouts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PRRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ به\u200cروزرسانی')),
                ('record_date', models.DateField(verbose_name='تاریخ ثبت رکورد')),
                ('max_weight_kg', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='حداکثر وزن (کیلوگرم)')),
                ('max_reps', models.PositiveIntegerField(blank=True, null=True, verbose_name='حداکثر تکرار')),
                ('min_time_seconds', models.PositiveIntegerField(blank=True, null=True, verbose_name='کمترین زمان (ثانیه)')),
                ('max_distance_km', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='بیشترین مسافت (کیلومتر)')),
                ('notes', models.TextField(blank=True, verbose_name='یادداشت\u200cها')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workouts.exercise', verbose_name='تمرین')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pr_records', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'رکورد شخصی',
                'verbose_name_plural': 'رکوردهای شخصی',
                'ordering': ['-record_date'],
            },
        ),
        migrations.CreateModel(
            name='DailyMood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ به\u200cروزرسانی')),
                ('date', models.DateField(unique=True, verbose_name='تاریخ')),
                ('mood_score', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='امتیاز حال و هوا')),
                ('notes', models.TextField(blank=True, verbose_name='یادداشت\u200cها')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_moods', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'حال و هوای روزانه',
                'verbose_name_plural': 'حال و هوای روزانه',
                'ordering': ['-date'],
                'unique_together': {('user', 'date')},
            },
        ),
        migrations.CreateModel(
            name='WeightLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ به\u200cروزرسانی')),
                ('date', models.DateField(verbose_name='تاریخ')),
                ('weight_kg', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='وزن (کیلوگرم)')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weight_logs', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'ثبت وزن',
                'verbose_name_plural': 'ثبت وزن',
                'ordering': ['-date'],
                'unique_together': {('user', 'date')},
            },
        ),
    ]
