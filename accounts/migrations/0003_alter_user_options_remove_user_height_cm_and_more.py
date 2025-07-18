# Generated by Django 5.2.3 on 2025-07-08 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_role_alter_user_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='height_cm',
        ),
        migrations.RemoveField(
            model_name='user',
            name='weight_kg',
        ),
        migrations.AddField(
            model_name='user',
            name='abdomen_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='دور شکم'),
        ),
        migrations.AddField(
            model_name='user',
            name='arm_l_biceps_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='دور بازوی چپ (بایسپس)'),
        ),
        migrations.AddField(
            model_name='user',
            name='arm_l_triceps_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='دور بازوی چپ (ترایسپس)'),
        ),
        migrations.AddField(
            model_name='user',
            name='arm_r_biceps_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='دور بازوی راست (بایسپس)'),
        ),
        migrations.AddField(
            model_name='user',
            name='arm_r_triceps_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='دور بازوی راست (ترایسپس)'),
        ),
        migrations.AddField(
            model_name='user',
            name='body_weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='وزن بدن'),
        ),
        migrations.AddField(
            model_name='user',
            name='calves_l_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='دور ساق پای چپ'),
        ),
        migrations.AddField(
            model_name='user',
            name='calves_r_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='دور ساق پای راست'),
        ),
        migrations.AddField(
            model_name='user',
            name='chest_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='دور سینه'),
        ),
        migrations.AddField(
            model_name='user',
            name='expertise_resume',
            field=models.TextField(blank=True, null=True, verbose_name='خلاصه تخصص و سابقه'),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'مرد'), ('female', 'زن')], max_length=10, null=True, verbose_name='جنسیت'),
        ),
        migrations.AddField(
            model_name='user',
            name='gym_experience_months',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='سابقه باشگاه (ماه)'),
        ),
        migrations.AddField(
            model_name='user',
            name='height',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='قد'),
        ),
        migrations.AddField(
            model_name='user',
            name='height_unit',
            field=models.CharField(blank=True, choices=[('cm', 'سانتی\u200cمتر'), ('inch', 'اینچ')], default='cm', max_length=5, null=True, verbose_name='واحد قد'),
        ),
        migrations.AddField(
            model_name='user',
            name='hip_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='دور باسن'),
        ),
        migrations.AddField(
            model_name='user',
            name='license',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='مجوز/گواهی\u200cنامه'),
        ),
        migrations.AddField(
            model_name='user',
            name='license_number',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='شماره مجوز'),
        ),
        migrations.AddField(
            model_name='user',
            name='neck_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='دور گردن'),
        ),
        migrations.AddField(
            model_name='user',
            name='shoulder_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='دور شانه'),
        ),
        migrations.AddField(
            model_name='user',
            name='thigh_l_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='دور ران چپ'),
        ),
        migrations.AddField(
            model_name='user',
            name='thigh_r_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='دور ران راست'),
        ),
        migrations.AddField(
            model_name='user',
            name='under_chest_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='دور زیر سینه (فقط برای خانم\u200cها)'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_position',
            field=models.CharField(blank=True, choices=[('client', 'ورزشکار/مشتری'), ('coach', 'مربی')], max_length=10, null=True, verbose_name='نقش کاربری در اپلیکیشن'),
        ),
        migrations.AddField(
            model_name='user',
            name='waist_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='دور کمر'),
        ),
        migrations.AddField(
            model_name='user',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('kg', 'کیلوگرم'), ('lbs', 'پوند')], default='kg', max_length=5, null=True, verbose_name='واحد وزن'),
        ),
    ]
