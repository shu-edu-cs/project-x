from django.contrib import admin
from django.http import JsonResponse
from simpleui.admin import AjaxAdmin
from borrow.models import BorrowBook
from django.db.models import Q
from datetime import datetime
from market.models import Book, MyBook, BookComment, SupportLog


@admin.register(Book)
class BookAdmin(AjaxAdmin):
    list_filter = ('status', 'create_user')
    search_fields = ('book_name', 'author')
    list_display = ('book_name', 'author', 'translator', 'status', 'create_user')
    fields = ('book_name', 'book_isbn', 'book_image', 'public_name', 'publish_year', 'author', 'translator', 'edition_order',
              'page_count',  'status', 'remark')
    list_per_page = 20

    def has_add_permission(self, request):
        """
        禁用添加按钮
        """
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or (obj and obj.create_user == request.user):
            return True
        else:
            return False

    # 重写编辑页, 继承父类方法
    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     def has_delete_permission(self, request, obj=None):
    #         return False
    #     self.has_delete_permission = has_delete_permission
    #     return super(BookAdmin, self).changeform_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return 'status', 'create_user'
        else:
            return 'create_user',

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

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
        # 这里的queryset 会有数据过滤，只包含选中的数据

        post = request.POST
        # 这里获取到数据后，可以做些业务处理
        # post中的_action 是方法名
        # post中 _selected 是选中的数据，逗号分割
        if not post.get('_selected'):
            return JsonResponse(data={
                'status': 'error',
                'msg': '请选择需要借的书！'
            })
        else:
            GMT_FORMAT = '%a %b %d %Y %H:%M:%S GMT+0800 (中国标准时间)'
            return_date = datetime.strptime(post.get('return_date'), GMT_FORMAT)
            if (return_date - datetime.now()).total_seconds() <= 0:
                return JsonResponse(data={
                    'status': 'error',
                    'msg': f'还书时间不能早于当前时间。'
                })
            for book in queryset:
                if book.create_user == request.user:

                    return JsonResponse(data={
                        'status': 'error',
                        'msg': f'您不能向自己借书《{book.book_name}》。'
                    })
                if book.status == 1:
                    return JsonResponse(data={
                        'status': 'error',
                        'msg': f'《{book.book_name}》已出借，请重新选择。'
                    })
                borrow_book_exists = BorrowBook.objects.filter(book=book, borrow_user=request.user, status__in=[0, 2, 3, 4]).first()
                if borrow_book_exists:
                    return JsonResponse(data={
                        'status': 'error',
                        'msg': f'您已提交《{book.book_name}》的借书请求，不要重复申请。'
                    })
                borrow_book = BorrowBook(book=book, lend_user=book.create_user, borrow_user=request.user,
                                         qq=post.get('qq'), wechat=post.get('wechat'), remark=post.get('remark'),
                                         return_date=return_date)
                borrow_book.save()
            return JsonResponse(data={
                'status': 'success',
                'msg': '申请成功，等待图书所有人处理！'
            })

    borrow_book.short_description = '借书'
    borrow_book.type = 'success'
    borrow_book.icon = 'el-icon-s-promotion'

    # 指定一个输入参数，应该是一个数组

    # 指定为弹出层，这个参数最关键
    borrow_book.layer = {
        # 弹出层中的输入框配置

        # 这里指定对话框的标题
        'title': '借书',
        # 提示信息
        'tips': '礼貌、友善的沟通方式更容易借书成功哦！',
        # 确认按钮显示文本
        'confirm_button': '确认借书',
        # 取消按钮显示文本
        'cancel_button': '取消',

        # 弹出层对话框的宽度，默认50%
        'width': '40%',

        # 表单中 label的宽度，对应element-ui的 label-width，默认80px
        'labelWidth': "80px",
        'params': [
            {
                # 这里的type 对应el-input的原生input属性，默认为input
                'type': 'input',
                # key 对应post参数中的key
                'key': 'qq',
                # 显示的文本
                'label': 'QQ',
                # 为空校验，默认为False
                'require': False
            },
            {
                # 这里的type 对应el-input的原生input属性，默认为input
                'type': 'input',
                # key 对应post参数中的key
                'key': 'wechat',
                # 显示的文本
                'label': '微信',
                # 为空校验，默认为False
                'require': False
            },
            {
                # 这里的type 对应el-input的原生input属性，默认为input
                'type': 'input',
                # key 对应post参数中的key
                'key': 'email',
                # 显示的文本
                'label': '邮箱',
                # 为空校验，默认为False
                'require': False
            },
            {
                # 这里的type 对应el-input的原生input属性，默认为input
                'type': 'input',
                # key 对应post参数中的key
                'key': 'remark',
                # 显示的文本
                'label': '说点什么',
                # 为空校验，默认为False
                'require': False
            },
            {
                'type': 'date',
                'key': 'return_date',
                'label': '还书时间',
                'require': True
            },
        ]
    }

    borrow_book.short_description = '借书'
    borrow_book.icon = 'fas el-icon-notebook-2'
    borrow_book.type = 'success'

    actions = ['borrow_book']


@admin.register(MyBook)
class MyBookAdmin(admin.ModelAdmin):
    list_filter = ('status', )
    search_fields = ('book_name', 'author')
    List_display_links = None
    list_display = ('book_name', 'author', 'translator', 'status')
    fields = ('book_name', 'book_isbn', 'public_name', 'publish_year', 'author', 'translator', 'edition_order',
              'page_count',  'status', 'remark')
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'create_user', None) is None:
            obj.create_user = request.user
        obj.save()

    def get_queryset(self, request):
        return Book.objects.filter(create_user=request.user)


@admin.register(BookComment)
class BookCommentAdmin(AjaxAdmin):
    search_fields = ('book', 'ip_address', 'nick_name', 'comment_content')
    list_display = ('book', 'ip_address', 'nick_name', 'comment_content', 'create_time')
    fields = ('book', 'ip_address', 'nick_name', 'comment_content')
    list_per_page = 20

    def has_add_permission(self, request):
        """
        禁用添加按钮
        """
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or (obj and obj.create_user == request.user):
            return True
        else:
            return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions


@admin.register(SupportLog)
class SupportLogAdmin(AjaxAdmin):
    search_fields = ('book', 'ip_address')
    list_display = ('book', 'ip_address')
    list_per_page = 20

    def has_add_permission(self, request):
        """
        禁用添加按钮
        """
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or (obj and obj.create_user == request.user):
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions