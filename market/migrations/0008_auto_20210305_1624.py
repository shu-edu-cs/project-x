# Generated by Django 3.1.5 on 2021-03-05 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0007_auto_20210223_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_image',
            field=models.ImageField(null=True, upload_to='book_image', verbose_name='图片'),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_num',
            field=models.CharField(default='fbce805d6dd249dcb4c06212146f914d', max_length=128, verbose_name='书号'),
        ),
    ]
