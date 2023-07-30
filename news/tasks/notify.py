from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL

def get_subscribers(category):
    user_emails = []
    for subscriber in category.subscribers.all():
        user_emails.append(subscriber.email)
    return user_emails


def create_post_notify(instance):
    for category in instance.category.all():
        user_emails = get_subscribers(category)

        html = render_to_string(
            'subscribe/create_post.html',
            {
                'category': category,
                'post': instance,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'New post in {category} category',
            from_email=DEFAULT_FROM_EMAIL,
            body='',
            to=user_emails
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()
