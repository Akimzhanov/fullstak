# Generated by Django 4.1.3 on 2022-11-30 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_card_alter_order_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='card',
            field=models.BigIntegerField(max_length=16),
        ),
    ]
