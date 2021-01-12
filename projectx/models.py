from django.db import models
from datetime import datetime


class BaseModel(models.Model):

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=datetime.now(), verbose_name='更新时间')


class Book(BaseModel):

    class Meta:
        verbose_name = '图书市场'
        verbose_name_plural = verbose_name

    book_num = models.CharField(max_length=128, null=False, verbose_name='书号')
    book_name = models.CharField(max_length=128, null=False, verbose_name='书名')
    book_isbn = models.CharField(max_length=128, null=True, verbose_name='ISBN')
    public_name = models.CharField(max_length=256, null=False, verbose_name='出版社名称')
    publish_year = models.CharField(max_length=16, null=True, verbose_name='出版年份')
    author = models.CharField(max_length=128, null=False, verbose_name='作者')
    translator = models.CharField(max_length=128, null=True, verbose_name='译者')
    edition_order = models.CharField(max_length=32, null=True, verbose_name='版次')
    page_count = models.SmallIntegerField(null=True, verbose_name='总页数')
    remark = models.CharField(max_length=512, null=True, verbose_name='备注')

    def __str__(self):
        return self.book_name



