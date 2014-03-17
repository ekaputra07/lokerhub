from __future__ import absolute_import

from django.core.mail import EmailMessage, mail_admins
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.timezone import now

import tweepy

from lokerhub.celery import app


@app.task
def task_send_moderation_email(job):
    """
    Send email to Admin when new job added.
    """
    try:
        mail_admins('New Job waiting for moderation - LokerHub',
                    settings.SITE_DOMAIN+reverse('admin:hub_job_change', args=(job.pk,)), fail_silently=True)
        return '[OK] Sending moderation email.'
    except Exception as e:
        return e


@app.task
def task_send_apply_email(job_application):
    """
    Send job application email task.
    """
    try:
        msg = EmailMessage('Job application for `%s` by %s via LokerHub' % (job_application.job.title, job_application.name),
                           job_application.coverletter,
                           job_application.email,
                           [job_application.company.email, job_application.job.user.email])

        msg.content_subtype = "html"  # Main content is now text/html
        if job_application.resume:
            msg.attach_file(job_application.resume.path)
        msg.send()
        return '[OK] Sending apllication email.'
    except Exception as e:
        return e


@app.task
def task_send_order_email(order):
    """
    Send Order email to admin and user task.
    """
    admin_message = render_to_string('emails/new-order-admin.html', {
                                        'job': order.job,
                                        'domain': settings.SITE_DOMAIN,
                                        'admin_link': reverse('admin:hub_premiumorder_change', args=[order.pk])
                                     })
    user_message = render_to_string('emails/new-order.html', {
                                        'user': order.user,
                                        'domain': settings.SITE_DOMAIN,
                                        'billing_link': reverse('billing'),
                                        'confirm_link': reverse('pay_confirm'),
                                    })
    try:
        # Send email to user
        user_msg = EmailMessage('Lowongan Premium `%s` - LokerHub' % order.job.title,
                                user_message, settings.ADMINS[0][1], [order.user.email])
        user_msg.send()

        # Send email to Admin
        mail_admins('Premium order `%s`- LokerHub' % order.job.title,
                    admin_message, fail_silently=True)
        return '[OK] Sending order email.'
    except Exception as e:
        return e


@app.task
def task_send_payconfirm_email(confirmation):
    """
    Send payment confirmation email to admin and user task.
    """
    admin_message = render_to_string('emails/new-payconfirm-admin.html', {
                                        'confirmation': confirmation,
                                        'domain': settings.SITE_DOMAIN,
                                        'admin_link': reverse('admin:hub_paymentconfirmation_change', args=[confirmation.pk])
                                     })
    user_message = render_to_string('emails/new-payconfirm.html', {
                                        'confirmation': confirmation,
                                        'domain': settings.SITE_DOMAIN,
                                    })
    try:
        # Send email to user
        user_msg = EmailMessage('Konfirmasi pembayaran `%s` - LokerHub' % confirmation.order.job.title,
                                user_message, settings.ADMINS[0][1], [confirmation.user.email])
        user_msg.send()

        # Send email to Admin
        mail_admins('Konfirmasi pembayaran `%s`- LokerHub' % confirmation.order.job.title,
                    admin_message, fail_silently=True)
        return '[OK] Sending PayConfirm email.'
    except Exception as e:
        return e


@app.task
def task_send_premium_activation_email(job):
    """
    Send user a notification about one of their job is now premium.
    """
    message = render_to_string('emails/premium-active.html', {
                                    'job': job,
                                    'domain': settings.SITE_DOMAIN,
                                })
    try:
        # Send email to user
        user_msg = EmailMessage('Premium telah aktif `%s` - LokerHub' % job.title,
                                message, settings.ADMINS[0][1], [job.user.email],
                                cc=[settings.ADMINS[0][1]])
        user_msg.send()
        return '[OK] Sending premium active email.'
    except Exception as e:
        return e


@app.task
def task_send_free_activation_email(job):
    """
    Send user a notification about one of their job is now approved.
    """
    message = render_to_string('emails/job-approved.html', {
                                    'job': job,
                                    'domain': settings.SITE_DOMAIN,
                                })
    try:
        # Send email to user
        user_msg = EmailMessage('Lowongan telah aktif `%s` - LokerHub' % job.title,
                                message, settings.ADMINS[0][1], [job.user.email],
                                cc=[settings.ADMINS[0][1]])
        user_msg.send()
        return '[OK] Sending approval email.'
    except Exception as e:
        return e


@app.task
def task_tweet_job(job):
    """
    Tweet new job.
    """
    consumer_key = settings.TWITTER_CONSUMER_KEY
    consumer_secret = settings.TWITTER_CONSUMER_SECRET
    access_token = settings.TWITTER_ACCESS_TOKEN
    access_token_secret = settings.TWITTER_TOKEN_SECRET

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    # If the application settings are set for "Read and Write" then
    # this line should tweet out the message to your account's 
    # timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
    try:
        status = 'Lowongan `%s` di %s %s%s via @LokerHub' % (job.title,
                                                             job.company,
                                                             settings.SITE_DOMAIN,
                                                             job.get_short_url())
        api.update_status(status)
        return '[OK] Tweet job.'
    except Exception as e:
        return e


@app.task
def task_periodic_check_jobtime():
    """
    Check job expiration.
    """
    try:
        from hub.models import Job
        jobs = Job.objects.filter(status='ACTIVE', ended__lte=now()).update(status='INACTIVE',
                                                                            is_premium=False)
        return '[OK] Job checks.'
    except Exception as e:
        return e