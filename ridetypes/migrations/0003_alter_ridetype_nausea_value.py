# Generated by Django 4.0.1 on 2022-02-04 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ridetypes', '0002_alter_ridename_excitement_modifier_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ridetype',
            name='nausea_value',
            field=models.SmallIntegerField(),
        ),
    ]
