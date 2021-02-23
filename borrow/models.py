from django.db import models
from market.models import BaseModel, Book
from django.conf import settings


# Create your models here.
class BorrowBook(BaseModel):

    class Meta:
        db_table = 'borrow_book'
        verbose_name = '借书记录'
        verbose_name_plural = verbose_name

    status_choices = ((0, '申请借书'), (1, '拒绝申请'), (2, '等待归还'), (3, '已经归还'))

    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='书籍')
    lend_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, verbose_name='出借人', related_name='lend_user')
    borrow_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, verbose_name='借书人', related_name='borrow_user')
    qq = models.CharField(null=True, blank=True, max_length=32, verbose_name='QQ')
    wechat = models.CharField(null=True, blank=True, max_length=32, verbose_name='微信')
    email = models.CharField(null=True,blank=True, max_length=64, verbose_name='Email')
    remark = models.CharField(null=True, blank=True, max_length=256, verbose_name='备注')
    return_date = models.DateField(null=False, blank=False, verbose_name='预计还书时间')
    real_return_date = models.DateField(null=False, blank=False, verbose_name='实际还书时间')
    status = models.SmallIntegerField(default=0, choices=status_choices, verbose_name='状态')


class BorrowComment(BaseModel):

    class Meta:
        db_table = 'borrow_comment'
        verbose_name = '借书评价'
        verbose_name_plural = verbose_name

    borrow = models.ForeignKey('BorrowBook', on_delete=models.CASCADE, verbose_name='借书记录')
    star = models.SmallIntegerField(null=False, blank=False, verbose_name='分数')
    comment = models.TextField(null=False, blank=False, verbose_name='评价内容')


class LendComment(BaseModel):

    class Meta:
        db_table = 'lend_comment'
        verbose_name = '出借评价'
        verbose_name_plural = verbose_name

    borrow = models.ForeignKey('BorrowBook', on_delete=models.CASCADE, verbose_name='借书记录')
    star = models.SmallIntegerField(null=False, blank=False, verbose_name='分数')
    comment = models.TextField(null=False, blank=False, verbose_name='评价内容')