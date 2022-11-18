# Generated by Django 4.1.3 on 2022-11-17 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('studios', '0006_alter_ammenityset_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('coach', models.CharField(max_length=50)),
                ('capacity', models.IntegerField()),
                ('weekday', models.CharField(max_length=10)),
                ('keywords', models.ManyToManyField(default=None, to='classes.keyword')),
                ('studio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='studios.studio')),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('date', models.DateField()),
                ('classes', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='classes.classes')),
                ('studio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='studios.studio')),
            ],
        ),
    ]
