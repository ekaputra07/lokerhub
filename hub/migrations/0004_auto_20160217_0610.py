# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0003_added_oneall_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='meta_desc',
            field=models.CharField(max_length=160, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_keys',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='job',
            name='meta_desc',
            field=models.CharField(max_length=160, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='job',
            name='meta_keys',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.ForeignKey(related_name='jobs', verbose_name=b'Perusahaan', to='hub.Company'),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(default=b'FULLTIME', max_length=15, verbose_name=b'Status karyawan', choices=[(b'FULLTIME', b'Full Time'), (b'PARTTIME', b'Part Time'), (b'FREELANCE', b'Freelance'), (b'INTERN', b'Magang'), (b'CONTRACT', b'Kontrak')]),
        ),
        migrations.AlterField(
            model_name='onealltoken',
            name='user',
            field=models.OneToOneField(related_name='oneall', to=settings.AUTH_USER_MODEL),
        ),
    ]
