# Generated by Django 4.2.4 on 2023-08-22 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('OWN', 'Own'), ('LOST', 'Lost'), ('FOUND', 'Found'), ('STOLEN', 'Stolen'), ('PENDING', 'Pending'), ('DELETED', 'Deleted')], max_length=10),
        ),
    ]