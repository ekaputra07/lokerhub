# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0004_auto_20160217_0610'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='salary_range',
            field=models.CharField(default=b'1J3', max_length=5, verbose_name=b'Kisaran gaji', choices=[(b'1J3', b'Rp. 1,000,000 - Rp. 3,000,000'), (b'3J5', b'RP. 3,000,000 - Rp. 5,000,000'), (b'5J10', b'Rp. 5,000,000 - Rp. 10,000,000'), (b'j10', b'Diatas Rp. 10,000,000'), (b'NEGO', b'Negosiasi')]),
        ),
    ]
