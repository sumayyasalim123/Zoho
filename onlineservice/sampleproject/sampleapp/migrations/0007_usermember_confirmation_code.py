# 0007_usermember_confirmation_code.py

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0006_alter_usermember1_confirmation_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermember',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
