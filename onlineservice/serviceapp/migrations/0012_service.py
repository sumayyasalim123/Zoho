# Generated by Django 5.0 on 2024-02-09 15:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapp', '0011_categories_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('description', models.CharField(max_length=255, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('duration', models.DurationField(null=True)),
                ('status', models.CharField(choices=[('1', 'Pending'), ('2', 'Approved'), ('3', 'Rejected')], default='1', max_length=1)),
                ('categories', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='serviceapp.categories')),
            ],
        ),
    ]
