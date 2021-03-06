# Generated by Django 4.0.5 on 2022-07-04 06:56

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
            name='Shape',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('type',
                 models.CharField(choices=[('triangle',
                                            'Triangle'),
                                           ('rectangle',
                                            'Rectangle'),
                                           ('square',
                                            'Square'),
                                           ('diamond',
                                            'Diamond')],
                                  default='triangle',
                                  max_length=20)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='shape',
            constraint=models.UniqueConstraint(
                fields=('name', 'user'), name='unique_shape_name'),
        ),
    ]
