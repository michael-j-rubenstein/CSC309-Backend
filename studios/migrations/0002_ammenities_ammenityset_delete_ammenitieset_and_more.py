# Generated by Django 4.1.3 on 2022-11-12 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ammenities',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='AmmenitySet',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('quanitity', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='AmmenitieSet',
        ),
        migrations.AlterField(
            model_name='studio',
            name='images',
            field=models.ImageField(upload_to='studios/images'),
        ),
        migrations.AddField(
            model_name='ammenityset',
            name='studio',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to='studios.studio'),
        ),
        migrations.AddField(
            model_name='ammenityset',
            name='type',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to='studios.ammenities'),
        ),
        migrations.RemoveField(
            model_name='studio',
            name='ammenities'
        ),
        migrations.AddField(
            model_name='studio',
            name='ammenities',
            field=models.ManyToManyField(
                blank=True, related_name='AmmenitySet', through='studios.AmmenitySet', to='studios.ammenities')
        )
    ]
