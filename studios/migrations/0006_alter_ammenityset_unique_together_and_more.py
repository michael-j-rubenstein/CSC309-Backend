# Generated by Django 4.1.3 on 2022-11-12 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0005_alter_studio_images'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ammenityset',
            unique_together={('studio', 'type')},
        ),
        migrations.AlterUniqueTogether(
            name='imageset',
            unique_together={('studio', 'image')},
        ),
    ]
