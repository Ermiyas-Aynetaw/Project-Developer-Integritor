# Generated by Django 4.1.3 on 2022-11-25 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_alter_review_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-vote_ratio', '-vote_total', 'title']},
        ),
    ]
