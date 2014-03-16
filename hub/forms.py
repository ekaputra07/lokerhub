import time

from django import forms
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

from hub.models import Company, Job, JobApplication, PremiumOrder, PaymentConfirmation


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, user, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError('Nama depan harus diisi.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError('Nama be;akang harus diisi.')
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                u = User.objects.get(email=email)
                if u != self.user:
                    raise forms.ValidationError('Email sudah terdaftar di akun lain.')
            except User.DoesNotExist:
                pass
        return email


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
