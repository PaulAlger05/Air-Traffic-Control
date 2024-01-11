# Generated by Django 4.2.5 on 2023-12-05 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atc_app', '0004_plane_pass_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='airline',
            name='id',
        ),
        migrations.RemoveField(
            model_name='airline',
            name='name',
        ),
        migrations.RemoveField(
            model_name='airport',
            name='id',
        ),
        migrations.RemoveField(
            model_name='gate',
            name='id',
        ),
        migrations.RemoveField(
            model_name='plane',
            name='id',
        ),
        migrations.RemoveField(
            model_name='runway',
            name='id',
        ),
        migrations.AlterField(
            model_name='airline',
            name='airlineID',
            field=models.CharField(max_length=5, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='airport',
            name='name',
            field=models.CharField(max_length=3, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='gate',
            name='gateID',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='plane',
            name='planeID',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='runway',
            name='runwayID',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, unique=True),
        ),
    ]