# Generated by Django 4.0.5 on 2022-06-20 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('duration', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('date', models.DateTimeField()),
                ('thumbnail', models.URLField()),
                ('description', models.CharField(blank=True, max_length=6000, null=True)),
            ],
        ),
    ]
