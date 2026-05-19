from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule


class Command(BaseCommand):
    help = 'Configura tarefas periodicas do Celery Beat'

    def handle(self, *args, **options):
        # Crontab: segunda-feira 9h (weekly reminder)
        schedule_reminder, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='9',
            day_of_week='1',  # segunda
            day_of_month='*',
            month_of_year='*',
        )

        PeriodicTask.objects.get_or_create(
            crontab=schedule_reminder,
            name='Weekly Reminder — Resumo Semanal',
            defaults={
                'task': 'api.tasks.send_weekly_reminder',
                'enabled': True,
            },
        )

        # Crontab: segunda-feira 10h (average alert)
        schedule_alert, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='10',
            day_of_week='1',  # segunda
            day_of_month='*',
            month_of_year='*',
        )

        PeriodicTask.objects.get_or_create(
            crontab=schedule_alert,
            name='Average Alert — Alerta de Gastos',
            defaults={
                'task': 'api.tasks.check_monthly_average',
                'enabled': True,
            },
        )

        self.stdout.write(self.style.SUCCESS('Tarefas periodicas configuradas com sucesso.'))
