# Generated by Django 2.0 on 2018-09-06 02:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('team', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstteam_goals', models.PositiveSmallIntegerField(default=0, verbose_name='T1 goals')),
                ('secondteam_goals', models.PositiveSmallIntegerField(default=0, verbose_name='T2 goals')),
                ('date_time', models.DateTimeField(auto_now_add=True, verbose_name='Finish-Date')),
                ('firstteam', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Team1', to='team.Team', verbose_name='Team 1')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('secondteam', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Team2', to='team.Team', verbose_name='Team 2')),
            ],
            options={
                'verbose_name_plural': 'Matches',
            },
        ),
    ]
