

from django.conf import settings
from django.db import migrations, models
import image_optimizer.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nickname', models.CharField(max_length=20, unique=True, verbose_name='nickname')),
                ('email', models.EmailField(blank=True, default='', max_length=255)),
                ('profile_img', image_optimizer.fields.OptimizedImageField(blank=True, null=True, upload_to='uploads/%Y/%m/%d')),
                ('bio', models.CharField(blank=True, default='', max_length=255)),
                ('mbti', models.CharField(blank=True, default='', max_length=4)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('followings', models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
