# Generated by Django 2.2.3 on 2019-09-03 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quality', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jirarole',
            name='id',
        ),
        migrations.AlterField(
            model_name='jirarole',
            name='jId',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]