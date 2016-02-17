# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0005_job_salary_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='education',
            field=models.SmallIntegerField(default=1, verbose_name=b'Pendidikan minimal', choices=[(1, b'Semua jenjang'), (2, b'SMP/sederajat'), (3, b'SMA/SMK/sederajat'), (4, b'Diploma D1/D2/D3'), (4, b'Sarjana/S1')]),
        ),
    ]
