# Generated by Django 5.2.3 on 2025-07-11 12:53

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progress_tracking', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailymood',
            name='date',
            field=models.DateField(verbose_name='تاریخ'),
        ),
        migrations.AlterField(
            model_name='prrecord',
            name='record_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='تاریخ ثبت رکورد'),
        ),
        migrations.CreateModel(
            name='DailyWaterLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ به\u200cروزرسانی')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='تاریخ')),
                ('amount_ml', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='مقدار آب (میلی\u200cلیتر)')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'ثبت آب روزانه',
                'verbose_name_plural': 'ثبت\u200cهای آب روزانه',
                'ordering': ['-date'],
                'unique_together': {('user', 'date')},
            },
        ),
    ]
