# Generated by Django 3.1.5 on 2021-02-23 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_auto_20210113_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_num',
            field=models.CharField(default='d88c0edae045489ea750c9b91f896409', max_length=128, verbose_name='书号'),
        ),
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '待出借'), (1, '已出借')], verbose_name='状态'),
        ),
    ]
