import uuid
from django.db import models
from datetime import datetime
from django.db.models import Q
from django.contrib import admin
from django.conf import settings


class BaseModel(models.Model):

    class Meta:
        abstract = True

    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, verbose_name='创建用户')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=datetime.now(), verbose_name='更新时间')


class Book(BaseModel):

    class Meta:
        db_table = 'market_book'
        verbose_name = '共享图书'
        verbose_name_plural = verbose_name

    book_num = models.CharField(max_length=128, default=uuid.uuid4().hex, null=False, blank=False, verbose_name='书号')
    book_name = models.CharField(max_length=128, null=False, blank=False, verbose_name='书名')
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
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None,
                                    verbose_name='共享人')

    def __str__(self):
        return self.book_name


class MyBook(Book):

    class Meta:
        proxy = True
        verbose_name = '我的共享'
        verbose_name_plural = verbose_name


@admin.register(MyBook)
class MyBookAdmin(admin.ModelAdmin):
    list_filter = ('status', )
    search_fields = ('book_name', 'author')
    list_display = ('book_name', 'author', 'translator', 'status')
    fields = ('book_name', 'book_isbn', 'public_name', 'publish_year', 'author', 'translator', 'edition_order',
              'page_count',  'status', 'remark')
    list_per_page = 20

    def has_delete_permission(self, request, obj=None):
        return True

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'create_user', None) is None:
            obj.create_user = request.user
        obj.save()

    def get_queryset(self, request):
        return Book.objects.filter(create_user=request.user)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_filter = ('status', 'create_user')
    search_fields = ('book_name', 'author')
    list_display = ('book_name', 'author', 'translator', 'status', 'create_user')
    fields = ('book_name', 'book_isbn', 'public_name', 'publish_year', 'author', 'translator', 'edition_order',
              'page_count',  'status', 'remark')
    list_per_page = 20

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return 'status', 'create_user'
        else:
            return 'create_user',

    def get_queryset(self, request):
        if not request.user.is_superuser:
            return Book.objects.filter(status=0).filter(~Q(create_user=request.user)).all()
        else:
            return Book.objects.all()

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'create_user', None) is None:
            obj.create_user = request.user
        obj.save()

    def borrow_book(self, request, queryset):
        pass

    borrow_book.short_description = '借书'
    borrow_book.icon = 'fas el-icon-notebook-2'
    borrow_book.type = 'success'

    actions = ['borrow_book']

