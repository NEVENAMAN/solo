# Generated by Django 2.2.4 on 2023-05-08 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appMain', '0012_products_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='certificate',
            field=models.ImageField(blank=True, default='', max_length=250, null=True, upload_to='certificates/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='photograph',
            field=models.ImageField(blank=True, default='', max_length=250, null=True, upload_to='doctors_image/'),
        ),
    ]