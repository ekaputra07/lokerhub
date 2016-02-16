from django.core.management.base import BaseCommand

from hub.models import IndeedJob

class Command(BaseCommand):
    help = 'Check for duplicate Indeed jobs and delete if any.'

    def handle(self, *args, **kwargs):
        IndeedJob.objects.raw("DELETE FROM indeed_jobs USING indeed_jobs as job2 WHERE indeed_jobs.id > job2.id AND indeed_jobs.jobkey = job2.jobkey")
