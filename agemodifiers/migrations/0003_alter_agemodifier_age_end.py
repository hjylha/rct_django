# Generated by Django 4.0.1 on 2022-02-04 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agemodifiers', '0002_rename_age_from_agemodifier_age_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agemodifier',
            name='age_end',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]