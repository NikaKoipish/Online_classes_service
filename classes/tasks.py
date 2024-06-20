from django.core.mail import send_mail
from celery import shared_task

from classes.models import Course
from config.settings import DEFAULT_FROM_EMAIL
from users.models import Subscription


@shared_task
def send_update_information(course_id):
    course = Course.objects.get(pk=course_id)
    subscribers = Subscription.objects.get(course=course_id)
    message = f'Курс {course.title} обновлен'
    send_mail(
        subject="Информирование об обновлении курса",
        message=f"Здравствуйте!\n"
                f"{message}",
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[subscribers.user.email, "nika.koipish@gmail.com"]
    )
