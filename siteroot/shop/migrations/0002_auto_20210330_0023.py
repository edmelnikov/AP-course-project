# Generated by Django 3.1.7 on 2021-03-29 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='in_stock',
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default='sample  text', max_length=2048),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='materials',
            field=models.CharField(default='sample  text', max_length=50),
            preserve_default=False,
        ),
    ]
