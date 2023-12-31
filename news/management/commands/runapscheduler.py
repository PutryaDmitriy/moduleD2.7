import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

from news.models import Post


DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL

logger = logging.getLogger(__name__)

def week_posts():
    posts = Post.objects.filter(pub_date__range=(datetime.now()-timedelta(days=7), datetime.now()))
    return posts

def get_subscribers(category):
    user_emails = []
    for subscriber in category.subscribers.all():
        user_emails.append(subscriber.email)
    return user_emails

# наша задача по выводу текста на экран
def my_job():
    #  Your job processing logic here...
    subscribe_dict = {}
    for post in week_posts():
        for category in post.category.all():
            if subscribe_dict.get(category):
                subscribe_dict[category].append(post)
            else:
                subscribe_dict[category] = [post]
    for key, value in subscribe_dict.items():
        user_emails = get_subscribers(key)

        html = render_to_string(
            'subscribe/week_posts.html',
            {
                'category': key,
                'posts': value,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Week posts in {key} category',
            from_email=DEFAULT_FROM_EMAIL,
            body='',
            to=user_emails
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()


# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")