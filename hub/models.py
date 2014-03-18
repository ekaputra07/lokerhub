import random
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.signals import request_finished
from django.conf import settings
from django.contrib.humanize.templatetags import humanize
from django.utils.timezone import now

from hub.utils import (send_apply_email, send_order_email, send_payconfirm_email,
                       tweet_job, send_moderation_email)


class SocialLoginProvider(models.Model):
    """
    User login provider.
    """
    user = models.ForeignKey(User)
    name = models.CharField(max_length=30)
    provider_user_id = models.CharField(max_length=200)

    class Meta:
        db_table = 'social_login_providers'
        verbose_name = 'Social Login Provider'
        verbose_name_plural = 'Social Login Providers'

    def __unicode__(self):
        return u'%s - %s' % (self.name, self.provider_user_id)


class Company(models.Model):
    """
    User company.
    """
    user = models.ForeignKey(User)
    name = models.CharField('Nama Perusahaan', max_length=200, default='')
    email = models.EmailField('Email (Lowongan akan dikirim ke email ini)', default='')
    phone = models.CharField('Telepon', max_length=50, blank=True, null=True, default='')
    address = models.CharField('Alamat', max_length=200, default='')
    city = models.CharField('Kota / Kabupaten', max_length=50, null=True, blank=True)
    state = models.CharField('Provinsi', max_length=50)
    website = models.URLField('Website', blank=True, null=True, default='')
    description = models.TextField('Keterangan perusahaan', default='')
    logo = models.ImageField('Logo (JPG/PNG)', upload_to='logos', blank=True, null=True)

    class Meta:
        db_table = 'companies'
        verbose_name_plural = 'Companies'
        ordering = ['-pk']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_edit_url(self):
        return ('company_edit', None, {'company_id': self.pk,})

    @models.permalink
    def get_delete_url(self):
        return ('company_delete', None, {'company_id': self.pk,})


class Category(models.Model):
    """
    Jobs category.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    indeed_query = models.CharField(max_length=50, null=True, blank=True)
    order = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_jobs_url(self):
        return ('jobs', None, {'category_slug': self.slug, })

    @models.permalink
    def get_skills_url(self):
        return ('skill', None, {'category_slug': self.slug, })

    @models.permalink
    def get_cron_url(self):
        return ('indeed_cron', None, {'category_id': self.pk, })


JOB_TYPES = (
    ('FULLTIME', 'Full Time'),
    ('PARTTIME', 'Part Time'),
    ('FREELANCE', 'Freelance'),
    ('INTERN', 'Magang'),
)

JOB_STATUSES = (
    ('PENDING', 'Pending'),
    ('ACTIVE', 'Aktif'),
    ('INACTIVE', 'Inactive'),
)

class Job(models.Model):
    """
    The job.
    """
    user = models.ForeignKey(User)
    status = models.CharField(max_length=15, choices=JOB_STATUSES, default='INACTIVE')
    approved = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True)

    is_premium = models.BooleanField('Premium', default=False)
    company = models.ForeignKey(Company, verbose_name='Perusahaan')
    title = models.CharField('Nama pekerjaan', max_length=150, default='')
    job_type = models.CharField('Status karyawan', max_length=15, choices=JOB_TYPES, default='FULLTIME')
    category = models.ForeignKey(Category, verbose_name='Kategori')
    location = models.CharField('Lokasi kerja', max_length=150, blank=True, null=True, default='')
    description = models.TextField('Deskripsi pekerjaan', default='')
    how_to_apply = models.TextField('Cara melamar', blank=True, null=True, default='')

    created = models.DateTimeField(auto_now_add=True, default=now)
    modified = models.DateTimeField(auto_now=True, default=now)
    started = models.DateTimeField(default=now)
    ended = models.DateTimeField(default=now)

    class Meta:
        db_table = 'jobs'
        ordering = ['-created']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = '%s%s-%s' % (self.user.pk, random.randint(100, 900), slugify(self.title))
        super(Job, self).save(*args, **kwargs)

    @models.permalink
    def get_edit_url(self):
        return ('job_edit', None, {'job_id': self.pk,})

    @models.permalink
    def get_delete_url(self):
        return ('job_delete', None, {'job_id': self.pk,})

    @models.permalink
    def get_absolute_url(self):
        return ('job_detail', None, {'job_slug': self.slug,})

    @models.permalink
    def get_short_url(self):
        return ('job_shortlink', None, {'job_id': self.pk,})

    @models.permalink
    def get_toggle_url(self):
        return ('job_toggle', None, {'job_id': self.pk,})

    @models.permalink
    def get_cancelpremium_url(self):
        return ('job_cancelpremium', None, {'job_id': self.pk,})

    @models.permalink
    def get_gopremium_url(self):
        return ('job_gopremium', None, {'job_id': self.pk,})

    @property
    def has_active_order(self):
        orders = self.premiumorder_set.filter(status='UNPAID')
        if len(orders):
            return True
        return False

models.signals.post_save.connect(send_moderation_email, sender=Job)


class JobApplication(models.Model):
    """
    Job applications.
    """
    company = models.ForeignKey(Company)
    job = models.ForeignKey(Job)
    name = models.CharField('Nama lengkap', max_length=100)
    email = models.EmailField('Email')
    resume = models.FileField('Upload Resume / CV', upload_to='resumes', blank=True, null=True)
    coverletter = models.TextField('Surat lamaran')
    read_status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, default=now)

    class Meta:
        db_table = 'job_applications'
        ordering = ['-created']

    def __unicode__(self):
        return u'%s to %s' % (self.name, self.company.name)

models.signals.post_save.connect(send_apply_email, sender=JobApplication)


class IndeedJob(models.Model):
    """
    Indeed Job.
    """
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=150, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    jobkey = models.CharField(max_length=150, blank=True, null=True)
    onmousedown = models.CharField(max_length=150, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=now, blank=True, null=True)

    class Meta:
        db_table = 'indeed_jobs'
        ordering = ['-created']

    def __unicode__(self):
        return self.title


ORDER_STATUSES = (
    ('UNPAID', 'Belum dibayar'),
    ('PAID', 'Sudah dibayar'),
    ('CANCELED', 'Dibatalkan'),
)

class PremiumOrder(models.Model):
    """
    Premium order.
    """
    user = models.ForeignKey(User)
    job = models.ForeignKey(Job, blank=True, null=True)
    job_title = models.CharField(max_length=150, default='')
    status  = models.CharField(max_length=15, choices=ORDER_STATUSES, default='UNPAID')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    unique_amount = models.DecimalField(max_digits=14, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True, default=now)
    updated = models.DateTimeField(auto_now=True, default=now)

    class Meta:
        db_table = 'premium_orders'

    def __unicode__(self):
        return self.job_title

models.signals.post_save.connect(send_order_email, sender=PremiumOrder)


def get_banks():
    return ((bank['name'], '%s (%s - %s)' % (bank['name'], bank['ac'], bank['an'])) for bank in settings.BANKS)

class PaymentConfirmation(models.Model):
    """
    Payment Confirmation for premium services.
    """
    user = models.ForeignKey(User)
    order = models.ForeignKey(PremiumOrder, verbose_name='Lowongan')
    bank_to = models.CharField('Bank tujuan transfer', max_length=15, choices=get_banks())
    from_bank = models.CharField('Bank asal transfer', max_length=50, default='')
    from_name = models.CharField('Nama pemilik rekening', max_length=150, default='')
    from_acc = models.CharField('No. rekening', max_length=50, default='')
    from_amount = models.CharField('Jumlah transfer', max_length=50, default=settings.PREMIUM_FEE)
    date = models.DateField('Tanggal transfer (Tanggal-Bulan-Tahun)', default=now)
    from_note = models.TextField('Catatan tambahan', blank=True, null=True, default='')
    created = models.DateTimeField(auto_now_add=True, default=now)
    checked = models.BooleanField(default=False)

    class Meta:
        db_table = 'payment_confirmations'
        ordering = ['-created']

    def __unicode__(self):
        return self.order.job.title

models.signals.post_save.connect(send_payconfirm_email, sender=PaymentConfirmation)
