# Generated by Django 4.1.4 on 2022-12-18 21:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at', models.DateTimeField(auto_now_add=True)),
                ('end_at', models.DateTimeField()),
                ('message', models.TextField()),
            ],
            options={
                'db_table': 'mailing',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('not_sent', 'Not Sent'), ('sent', 'Sent'), ('delivered', 'Delivered'), ('failed', 'Failed')], default='not_sent', max_length=255)),
                ('mailing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='mailings.mailing')),
            ],
            options={
                'db_table': 'message',
            },
        ),
    ]
