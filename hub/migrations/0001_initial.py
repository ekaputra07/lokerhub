# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('indeed_query', models.CharField(max_length=50, null=True, blank=True)),
                ('order', models.IntegerField(default=0, null=True, blank=True)),
            ],
            options={
                'db_table': 'categories',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=200, verbose_name=b'Nama Perusahaan')),
                ('email', models.EmailField(default=b'', max_length=254, verbose_name=b'Email (Lowongan akan dikirim ke email ini)')),
                ('phone', models.CharField(default=b'', max_length=50, null=True, verbose_name=b'Telepon', blank=True)),
                ('address', models.CharField(default=b'', max_length=200, verbose_name=b'Alamat')),
                ('city', models.CharField(max_length=50, null=True, verbose_name=b'Kota / Kabupaten', blank=True)),
                ('state', models.CharField(max_length=50, verbose_name=b'Provinsi')),
                ('website', models.URLField(default=b'', null=True, verbose_name=b'Website', blank=True)),
                ('description', models.TextField(default=b'', verbose_name=b'Keterangan perusahaan')),
                ('logo', models.ImageField(upload_to=b'logos', null=True, verbose_name=b'Logo (JPG/PNG)', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-pk'],
                'db_table': 'companies',
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='IndeedJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150, null=True, blank=True)),
                ('company', models.CharField(max_length=150, null=True, blank=True)),
                ('location', models.CharField(max_length=150, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('jobkey', models.CharField(max_length=150, null=True, blank=True)),
                ('onmousedown', models.CharField(max_length=150, null=True, blank=True)),
                ('url', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)),
                ('category', models.ForeignKey(to='hub.Category')),
            ],
            options={
                'ordering': ['-created'],
                'db_table': 'indeed_jobs',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'INACTIVE', max_length=15, choices=[(b'PENDING', b'Pending'), (b'ACTIVE', b'Aktif'), (b'INACTIVE', b'Inactive')])),
                ('approved', models.BooleanField(default=False)),
                ('slug', models.SlugField(null=True, blank=True)),
                ('ads_type', models.SmallIntegerField(default=1)),
                ('title', models.CharField(default=b'', max_length=150, verbose_name=b'Nama pekerjaan')),
                ('job_type', models.CharField(default=b'FULLTIME', max_length=15, verbose_name=b'Status karyawan', choices=[(b'FULLTIME', b'Full Time'), (b'PARTTIME', b'Part Time'), (b'FREELANCE', b'Freelance'), (b'INTERN', b'Magang')])),
                ('location', models.CharField(default=b'', max_length=150, null=True, verbose_name=b'Lokasi kerja', blank=True)),
                ('description', models.TextField(default=b'', verbose_name=b'Deskripsi pekerjaan')),
                ('how_to_apply', models.TextField(default=b'', null=True, verbose_name=b'Cara melamar', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('started', models.DateTimeField(default=django.utils.timezone.now)),
                ('ended', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(verbose_name=b'Kategori', to='hub.Category')),
                ('company', models.ForeignKey(verbose_name=b'Perusahaan', to='hub.Company')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'db_table': 'jobs',
            },
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'Nama lengkap')),
                ('email', models.EmailField(max_length=254, verbose_name=b'Email')),
                ('resume', models.FileField(upload_to=b'resumes', null=True, verbose_name=b'Upload Resume / CV', blank=True)),
                ('coverletter', models.TextField(verbose_name=b'Surat lamaran')),
                ('read_status', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(to='hub.Company')),
                ('job', models.ForeignKey(to='hub.Job')),
            ],
            options={
                'ordering': ['-created'],
                'db_table': 'job_applications',
            },
        ),
        migrations.CreateModel(
            name='PaymentConfirmation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bank_to', models.CharField(max_length=15, verbose_name=b'Bank tujuan transfer', choices=[(b'BCA', b'BCA (135.024.2593 - Pande Putu Eka Putra)')])),
                ('from_bank', models.CharField(default=b'', max_length=50, verbose_name=b'Bank asal transfer')),
                ('from_name', models.CharField(default=b'', max_length=150, verbose_name=b'Nama pemilik rekening')),
                ('from_acc', models.CharField(default=b'', max_length=50, verbose_name=b'No. rekening')),
                ('from_amount', models.CharField(default=100000, max_length=50, verbose_name=b'Jumlah transfer')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name=b'Tanggal transfer (Tanggal-Bulan-Tahun)')),
                ('from_note', models.TextField(default=b'', null=True, verbose_name=b'Catatan tambahan', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('checked', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-created'],
                'db_table': 'payment_confirmations',
            },
        ),
        migrations.CreateModel(
            name='PremiumOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_title', models.CharField(default=b'', max_length=150)),
                ('status', models.CharField(default=b'UNPAID', max_length=15, choices=[(b'UNPAID', b'Belum dibayar'), (b'PAID', b'Sudah dibayar'), (b'CANCELED', b'Dibatalkan')])),
                ('amount', models.DecimalField(max_digits=14, decimal_places=2)),
                ('unique_amount', models.DecimalField(max_digits=14, decimal_places=2)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(blank=True, to='hub.Job', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'premium_orders',
            },
        ),
        migrations.CreateModel(
            name='SocialLoginProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('provider_user_id', models.CharField(max_length=200)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'social_login_providers',
                'verbose_name': 'Social Login Provider',
                'verbose_name_plural': 'Social Login Providers',
            },
        ),
        migrations.AddField(
            model_name='paymentconfirmation',
            name='order',
            field=models.ForeignKey(verbose_name=b'Lowongan', to='hub.PremiumOrder'),
        ),
        migrations.AddField(
            model_name='paymentconfirmation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
