# Generated by Django 4.2.4 on 2023-08-20 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booksapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='name_author',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='borrowrequest',
            name='request_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='borrowrequest',
            name='status',
            field=models.IntegerField(choices=[(1, 'PENDING'), (2, 'APPROVED'), (3, 'COLLECTED'), (4, 'COMPLETE'), (5, 'DECLINED')], default=1),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name_genre',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
