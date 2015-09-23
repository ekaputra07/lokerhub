# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hub', '0002_remove_old_social_login_provider'),
    ]

    operations = [
        migrations.CreateModel(
            name='OneallToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(related_name='token', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'oneall_tokens',
                'verbose_name': 'OneAll Token',
                'verbose_name_plural': 'OneAll Tokens',
            },
        ),
    ]
