from django.contrib import admin
from hub.models import (SocialLoginProvider, Company, Category, Job,
                        JobApplication, IndeedJob, PremiumOrder, PaymentConfirmation)


admin.site.register(SocialLoginProvider)
admin.site.register(Company)
admin.site.register(Category)
admin.site.register(Job)
admin.site.register(JobApplication)
admin.site.register(IndeedJob)
admin.site.register(PremiumOrder)
admin.site.register(PaymentConfirmation)