# Generated by Django 4.1.1 on 2022-09-07 10:07

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_product_slug_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_information',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
