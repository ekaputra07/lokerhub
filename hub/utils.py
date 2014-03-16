import datetime
import pytz

from hub.tasks import (task_send_apply_email, task_send_order_email, 
                       task_send_payconfirm_email, task_send_premium_activation_email,
                       task_send_free_activation_email, task_tweet_job)


def send_apply_email(sender, instance, created, **kwargs):
    """
    Send email to company.
    """
    if created:
        task_send_apply_email.delay(instance)


def send_order_email(sender, instance, created, **kwargs):
    """
    Send Order email to admin and user.
    """
    if created:
        task_send_order_email.delay(instance)


def send_payconfirm_email(sender, instance, created, **kwargs):
    """
    Send payment confirmation email to admin and user.
    """
    if created:
        task_send_payconfirm_email.delay(instance)


def tweet_job(sender, instance, created, **kwargs):
    """
    Tweet the new job.
    """
    if created:
        task_tweet_job.delay(instance)


def send_premium_activation_email(job):
    """
    Send user a notification about one of their job is now premium.
    """
    task_send_premium_activation_email.delay(job)


def send_free_activation_email(job):
    """
    Send user a notification about one of their job is now approved.
    """
    task_send_free_activation_email.delay(job)


def convert_gtm_to_utc(gmt_string):
    """
    Convert GMT time to UTC
    """ 
    gmt = pytz.timezone('GMT')
    utc = pytz.timezone('UTC')
    date = datetime.datetime.strptime(gmt_string, '%a, %d %b %Y %H:%M:%S GMT')
    date_gmt = gmt.localize(date)
    date_utc = date_gmt.astimezone(utc)
    return date_utc
