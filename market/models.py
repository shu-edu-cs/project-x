import uuid
from django.db import models
from datetime import datetime
from django.conf import settings


class BaseModel(models.Model):

    class Meta:
        abstract = True

    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True, verbose_name='创建用户')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=datetime.now(), verbose_name='更新时间')


class Book(BaseModel):

    class Meta:
        db_table = 'market_book'
        verbose_name = '共享图书'
        verbose_name_plural = verbose_name

    book_num = models.CharField(max_length=128, default=uuid.uuid4().hex, null=False, blank=False, verbose_name='书号')
    book_name = models.CharField(max_length=128, null=False, blank=False, verbose_name='书名')
    book_image = models.ImageField(upload_to='static/book_image', verbose_name='图片', null=True, blank=True)
    book_isbn = models.CharField(max_length=128, null=False, blank=False, verbose_name='ISBN')
    public_name = models.CharField(max_length=256, null=True, blank=True, verbose_name='出版社名称')
    publish_year = models.CharField(max_length=16, null=True, blank=True, verbose_name='出版年份')
    author = models.CharField(max_length=128, null=False, blank=False, verbose_name='作者')
    translator = models.CharField(max_length=128, null=True, blank=True, verbose_name='译者')
    edition_order = models.CharField(max_length=32, null=True, blank=True, verbose_name='版次')
    page_count = models.SmallIntegerField(null=True, blank=True, verbose_name='总页数')
    status_type = ((0, '待出借'), (1, '已出借'))
    status = models.SmallIntegerField(null=False, verbose_name='状态', choices=status_type)
    remark = models.TextField(max_length=512, null=True, blank=True, verbose_name='备注')
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, verbose_name='共享人')

    def __str__(self):
        return self.book_name


class MyBook(Book):

    class Meta:
        proxy = True
        verbose_name = '我的共享'
        verbose_name_plural = verbose_name


class BookComment(models.Model):

    class Meta:
        db_table = 'book_comment'
        verbose_name = '图书评论'
        verbose_name_plural = verbose_name

    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='书籍')
    ip_address = models.CharField(max_length=128, null=False, blank=False, verbose_name='IP地址')
    nick_name = models.CharField(max_length=128, null=False, blank=False, verbose_name='昵称')
    comment_content = models.CharField(max_length=512, null=False, blank=False, verbose_name='评论内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class SupportLog(models.Model):

    class Meta:
        db_table = 'support_log'
        verbose_name = '点赞记录'
        verbose_name_plural = verbose_name

    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='书籍')
    ip_address = models.CharField(max_length=128, null=False, blank=False, verbose_name='IP地址')
