# Generated by Django 4.1.1 on 2022-12-03 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sportsapp', '0002_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fixture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('teamID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sportsapp.team')),
            ],
        ),
    ]
