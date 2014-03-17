from django.conf.urls import patterns, include, url

urlpatterns = patterns('hub.views',
    url(r'^$', 'home_view', name='home'),
    url(r'^robots.txt$', 'robots_txt', name='robots_txt'),
    url(r'^about/$', 'page_about', name='page_about'),
    url(r'^faq/$', 'page_faq', name='page_faq'),
    url(r'^contact/$', 'page_contact', name='page_contact'),

    url(r'^login/$', 'login_view', name='login'),
    url(r'^login/callback/$', 'logincallback_view', name='login_callback'),
    url(r'^logout/$', 'logout_view', name='logout'),
    url(r'^cron/links/$', 'indeed_cron_links', name='indeed_cron_links'),
    url(r'^cron/indeed/(?P<category_id>\d+)/$', 'indeed_cron_view', name='indeed_cron'),
    url(r'^dashboard/$', 'dashboard_view', name='dashboard'),
    url(r'^dashboard/profile/$', 'profile_view', name='edit_profile'),
    url(r'^dashboard/billing/$', 'billing_view', name='billing'),
    url(r'^dashboard/payment-confirmation/$', 'payconfirm_view', name='pay_confirm'),
    url(r'^dashboard/payment-valid/(?P<order_id>\d+)/$', 'payment_valid_view', name='payment_valid'),
    url(r'^dashboard/activate-free/(?P<job_id>\d+)/$', 'activate_free_view', name='activate_free'),
    url(r'^dashboard/activate-premium/(?P<job_id>\d+)/$', 'activate_premium_view', name='activate_premium'),

    url(r'^dashboard/companies/$', 'companies_view', name='companies'),
    url(r'^dashboard/companies/new/$', 'company_new_view', name='company_new'),
    url(r'^dashboard/companies/(?P<company_id>\d+)/edit/$', 'company_edit_view', name='company_edit'),
    url(r'^dashboard/companies/(?P<company_id>\d+)/delete/$', 'company_delete_view', name='company_delete'),

    url(r'^dashboard/jobs/new/$', 'job_new_view', name='job_new'),
    url(r'^dashboard/jobs/(?P<job_id>\d+)/edit/$', 'job_edit_view', name='job_edit'),
    url(r'^dashboard/jobs/(?P<job_id>\d+)/delete/$', 'job_delete_view', name='job_delete'),
    url(r'^dashboard/jobs/(?P<job_id>\d+)/toggle/$', 'job_toggle_view', name='job_toggle'),
    url(r'^dashboard/jobs/(?P<job_id>\d+)/go-premium/$', 'job_gopremium_view', name='job_gopremium'),
    url(r'^dashboard/jobs/(?P<job_id>\d+)/cancel-premium/$', 'job_cancelpremium_view', name='job_cancelpremium'),

    url(r'^jobs/(?P<job_slug>[\w-]+)/$', 'job_detail_view', name='job_detail'),
    url(r'^j/(?P<job_id>\d+)/$', 'job_shortlink_view', name='job_shortlink'),
    url(r'^indeed/(?P<category_id>\d+)/ajax/$', 'indeed_jobs', name='indeed_jobs'),
    url(r'^(?P<category_slug>[\w-]+)/$', 'jobs_view', name='jobs'),
)
