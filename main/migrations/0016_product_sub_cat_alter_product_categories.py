# Generated by Django 4.1.1 on 2022-10-02 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_coupon_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sub_cat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.sub_category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.category'),
        ),
    ]