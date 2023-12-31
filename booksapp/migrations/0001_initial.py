# Generated by Django 4.2.4 on 2023-08-19 13:38

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
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_author', models.CharField(max_length=255)),
                ('bio_author', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(max_length=255)),
                ('book_summary', models.TextField()),
                ('isbn', models.CharField(unique=True)),
                ('is_available', models.BooleanField(default=True)),
                ('published_date', models.DateField()),
                ('publisher_book', models.CharField(max_length=255)),
                ('book_authors', models.ManyToManyField(to='booksapp.author')),
                ('book_borrower', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_genre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='BorrowRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overdue', models.BooleanField(default=False)),
                ('request_date', models.DateTimeField()),
                ('due_date', models.DateField(blank=True, null=True)),
                ('complete_date', models.DateField(blank=True, null=True)),
                ('status', models.IntegerField(default=1)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booksapp.book')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='book_genre',
            field=models.ManyToManyField(blank=True, to='booksapp.genre'),
        ),
    ]
