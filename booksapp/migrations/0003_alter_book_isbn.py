# Generated by Django 4.2.4 on 2023-08-20 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booksapp', '0002_alter_author_name_author_alter_book_isbn_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(unique=True),
        ),
    ]
