

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movie_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('poster', models.TextField()),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MovieLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('love', models.BooleanField(default=False)),
                ('like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, through='movies.MovieLike', to=settings.AUTH_USER_MODEL),
        ),
    ]
