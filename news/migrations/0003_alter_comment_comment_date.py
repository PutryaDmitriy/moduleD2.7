# Generated by Django 4.1.7 on 2023-03-07 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_comment_comment_date_alter_post_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
