# Generated by Django 2.2.6 on 2019-10-21 17:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('first_name', models.CharField(max_length=255, verbose_name='First Name')),
                ('last_name', models.CharField(default='', max_length=255, null=True, verbose_name='Last Name')),
                ('phone_number', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='Phone Number')),
                ('uuid', models.UUIDField(default=uuid.uuid4, verbose_name='UUID')),
            ],
            options={
                'verbose_name': 'contacts',
                'verbose_name_plural': 'contacts',
                'db_table': 'contacts',
            },
        ),
    ]
