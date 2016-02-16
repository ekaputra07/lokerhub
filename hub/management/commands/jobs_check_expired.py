from django.core.management.base import BaseCommand

from hub.tasks import task_periodic_check_jobtime

class Command(BaseCommand):
    help = 'Check for expired jobs and set inactive if any.'

    def handle(self, *args, **kwargs):
        task_periodic_check_jobtime.delay()
