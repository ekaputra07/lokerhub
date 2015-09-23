from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from hub.models import (OneallToken, Company, Category, Job,
                        JobApplication, IndeedJob, PremiumOrder, PaymentConfirmation)



class OneallTokenAdmin(admin.TabularInline):
    model = OneallToken
    can_delete = False

class UserAdmin(UserAdmin):
    inlines = [OneallTokenAdmin]
    save_on_top = True

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'email', 'address', 'website']
    save_on_top = True
    search_fields = ['name', 'user__username']

admin.site.register(Company, CompanyAdmin)


class CategoryAdmn(admin.ModelAdmin):
    list_display = ['name', 'indeed_query', 'order']
    list_editable = ['order']
    save_on_top = True

admin.site.register(Category, CategoryAdmn)


class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'approved', 'ads_type', 'company', 'started', 'ended']
    save_on_top = True
    search_fields = ['title', 'user__username', 'company__name']
    list_filter = ('status', 'approved', 'ads_type', 'started', 'ended')

admin.site.register(Job, JobAdmin)


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'job', 'company', 'resume', 'read_status']
    save_on_top = True
    search_fields = ['name', 'job__title', 'company__name', 'email']
    list_filter = ('read_status',)

admin.site.register(JobApplication, JobApplicationAdmin)


class IndeedJobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'jobkey', 'category']
    save_on_top = True
    search_fields = ['title', 'company', 'location', 'jobkey']
    list_filter = ('category__name',)

admin.site.register(IndeedJob, IndeedJobAdmin)


class PremiumOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'job_title', 'status', 'amount', 'created']
    save_on_top = True
    search_fields = ['user__username', 'job_title']
    list_filter = ('status',)

admin.site.register(PremiumOrder, PremiumOrderAdmin)


class PaymentConfirmationAdmin(admin.ModelAdmin):
    list_display = ['user', 'checked', 'order', 'from_bank', 'from_name', 'from_acc', 'from_amount', 'date', 'from_note']
    save_on_top = True
    search_fields = ['user__username', 'from_bank', 'from_name', 'from_acc']
    list_filter = ('checked', 'date',)

admin.site.register(PaymentConfirmation, PaymentConfirmationAdmin)
