from django.contrib import admin
from .models import BorrowBook, LendBook
from simpleui.admin import AjaxAdmin
from django.http import JsonResponse
from datetime import datetime


@admin.register(BorrowBook)
class BorrowBookAdmin(AjaxAdmin):
    list_filter = ('status', 'create_user')
    search_fields = ('book_name', 'author')
    list_display = ('book', 'lend_user', 'borrow_user', 'return_date', 'real_return_date', 'status')
    list_per_page = 20

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

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
                if book.status == 1:
                    return JsonResponse(data={
                        'status': 'error',
                        'msg': f'《{book.book_name}》已出借，请重新选择。'
                    })
                borrow_book_exists = BorrowBook.objects.filter(book=book,  borrow_user=request.user).first()
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

    borrow_book.short_description = '出借'
    borrow_book.type = 'success'
    borrow_book.icon = 'el-icon-s-promotion'

    actions = ['borrow_book']


@admin.register(LendBook)
class LendBookAdmin(AjaxAdmin):
    list_filter = ('status', 'create_user')
    search_fields = ('book_name', 'author')
    list_display = ('book', 'lend_user', 'borrow_user', 'return_date', 'real_return_date', 'status')
    list_per_page = 20

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

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
                if book.status == 1:
                    return JsonResponse(data={
                        'status': 'error',
                        'msg': f'《{book.book_name}》已出借，请重新选择。'
                    })
                borrow_book_exists = BorrowBook.objects.filter(book=book,  borrow_user=request.user).first()
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

    borrow_book.short_description = '还书'
    borrow_book.type = 'success'
    borrow_book.icon = 'el-icon-s-promotion'

    actions = ['borrow_book']
