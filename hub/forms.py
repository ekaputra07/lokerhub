import time

from django import forms
from django.db import models
from django.utils.timezone import now

from hub.models import Company, Job, JobApplication, PremiumOrder, PaymentConfirmation


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('user', 'logo')


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('user', 'status', 'slug', 'created', 'modified', 'started', 'ended', 'is_premium',)

    def __init__(self, user, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

        self.fields['company'].queryset = Company.objects.filter(user=user)


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        exclude = ('company', 'job', 'read_status', 'created',)


class PaymentConfirmationForm(forms.ModelForm):
    date = forms.DateField(input_formats=('%d/%m/%Y',), label='Tanggal transfer (Tanggal/Bulan/Tahun)', initial=now().strftime('%d/%m/%Y'))

    class Meta:
        model = PaymentConfirmation
        exclude = ('user',)

    def __init__(self, user, *args, **kwargs):
        super(PaymentConfirmationForm, self).__init__(*args, **kwargs)
        self.fields['order'].queryset = PremiumOrder.objects.filter(user=user, status='UNPAID')
