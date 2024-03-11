# Generated by Django 4.2.6 on 2023-11-03 08:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Courses', '0017_alter_applications_phonenumber_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='Likes_count',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='ChapterLiked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_liked', models.BooleanField(default=False)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Courses.chapter')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
