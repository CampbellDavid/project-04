# Generated by Django 2.2.9 on 2020-02-27 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20200227_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='sport',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='sports.Sport'),
        ),
    ]
