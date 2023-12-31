# Generated by Django 4.2.4 on 2023-08-22 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booksapp', '0003_alter_book_isbn'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['name_author']},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['book_title']},
        ),
        migrations.AlterField(
            model_name='borrowrequest',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrow_requests', to='booksapp.book'),
        ),
    ]
