# Generated by Django 5.1.7 on 2025-04-02 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cartitem_color_cartitem_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('in_process', 'In_process'), ('checked_out', 'Checked Out')], default='active', max_length=20),
        ),
    ]
