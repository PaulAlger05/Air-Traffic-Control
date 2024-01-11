# Generated by Django 4.2.5 on 2023-12-05 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('atc_app', '0008_remove_plane_airline_remove_plane_destination_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plane',
            name='airline',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='atc_app.airline'),
        ),
        migrations.AddField(
            model_name='plane',
            name='destination',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plane_dest', to='atc_app.airport'),
        ),
        migrations.AddField(
            model_name='plane',
            name='gate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='atc_app.gate'),
        ),
        migrations.AddField(
            model_name='plane',
            name='origin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plane_origin', to='atc_app.airport'),
        ),
        migrations.AddField(
            model_name='plane',
            name='runway',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='atc_app.runway'),
        ),
    ]
