from django.contrib import admin
from .models import BorrowBook, LendBook, BorrowComment, LendComment
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

    def lend_book(self, request, queryset):
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
            for _borrow_book in queryset:
                if _borrow_book.status != 0:
                    return JsonResponse(data={
                        'status': 'error',
                        'msg': f'《{_borrow_book.book.book_name}》不是可出借状态，请重新选择。'
                    })
                _borrow_book.book.status = 1
                _borrow_book.book.save()
                _borrow_book.status = 2
                _borrow_book.save()
            return JsonResponse(data={
                'status': 'success',
                'msg': '申请成功，等待图书所有人处理！'
            })

    lend_book.layer = {
        # 弹出层中的输入框配置

        # 这里指定对话框的标题
        'title': '确认出借',
        # 提示信息
        'tips': '记得和借书人约定一个取书方式哦！',
        # 确认按钮显示文本
        'confirm_button': '确认出借',
        # 取消按钮显示文本
        'cancel_button': '取消',

        # 弹出层对话框的宽度，默认50%
        'width': '40%',

        # 表单中 label的宽度，对应element-ui的 label-width，默认80px
        'labelWidth': "80px",
        # 'params': [
        #     {
        #         # 这里的type 对应el-input的原生input属性，默认为input
        #         'type': 'input',
        #         # key 对应post参数中的key
        #         'key': 'qq',
        #         # 显示的文本
        #         'label': 'QQ',
        #         # 为空校验，默认为False
        #         'require': False
        #     },
        #     {
        #         # 这里的type 对应el-input的原生input属性，默认为input
        #         'type': 'input',
        #         # key 对应post参数中的key
        #         'key': 'wechat',
        #         # 显示的文本
        #         'label': '微信',
        #         # 为空校验，默认为False
        #         'require': False
        #     },
        #     {
        #         # 这里的type 对应el-input的原生input属性，默认为input
        #         'type': 'input',
        #         # key 对应post参数中的key
        #         'key': 'email',
        #         # 显示的文本
        #         'label': '邮箱',
        #         # 为空校验，默认为False
        #         'require': False
        #     },
        #     {
        #         # 这里的type 对应el-input的原生input属性，默认为input
        #         'type': 'input',
        #         # key 对应post参数中的key
        #         'key': 'remark',
        #         # 显示的文本
        #         'label': '说点什么',
        #         # 为空校验，默认为False
        #         'require': False
        #     },
        #     {
        #         'type': 'date',
        #         'key': 'return_date',
        #         'label': '还书时间',
        #         'require': True
        #     },
        # ]
    }

    lend_book.short_description = '确认出借'
    lend_book.type = 'success'
    lend_book.icon = 'el-icon-s-promotion'

    def return_book(self, request, queryset):
        # 这里的queryset 会有数据过滤，只包含选中的数据

        post = request.POST
        # 这里获取到数据后，可以做些业务处理
        # post中的_action 是方法名
        # post中 _selected 是选中的数据，逗号分割
        if not post.get('_selected'):
            return JsonResponse(data={
                'status': 'error',
                'msg': '选择需要确认归还的书！'
            })
        else:
            for _borrow_book in queryset:
                if _borrow_book.status != 4:
                    return JsonResponse(data={
                        'status': 'error',
                        'msg': f'《{_borrow_book.book.book_name}》不是可确认归还的状态，请重新选择。'
                    })
                _borrow_book.book.status = 0
                _borrow_book.book.save()
                _borrow_book.status = 5
                _borrow_book.real_return_date = datetime.now()
                _borrow_book.save()
            return JsonResponse(data={
                'status': 'success',
                'msg': '已确认归还图书。'
            })

    return_book.layer = {
        # 弹出层中的输入框配置

        # 这里指定对话框的标题
        'title': '确认归还',
        # 提示信息
        'tips': '收到借书人归还的书再点击确认，以保障自己的权益！',
        # 确认按钮显示文本
        'confirm_button': '我已收到书',
        # 取消按钮显示文本
        'cancel_button': '取消',

        # 弹出层对话框的宽度，默认50%
        'width': '40%',

        # 表单中 label的宽度，对应element-ui的 label-width，默认80px
        'labelWidth': "80px"
    }
    return_book.short_description = '确认归还'
    return_book.type = 'success'
    return_book.icon = 'el-icon-s-promotion'

    def borrow_comment(self, request, queryset):
        # 这里的queryset 会有数据过滤，只包含选中的数据
        post = request.POST
        # 这里获取到数据后，可以做些业务处理
        # post中的_action 是方法名
        # post中 _selected 是选中的数据，逗号分割
        if not post.get('_selected'):
            return JsonResponse(data={
                'status': 'error',
                'msg': '选择需要评价的记录'
            })
        else:
            for _borrow_book in queryset:
                if _borrow_book.status != 5:
                    return JsonResponse(data={
                        'status': 'error',
                        'msg': f'《{_borrow_book.book.book_name}》需要等待对方还书后才可评价。'
                    })
                elif BorrowComment.objects.filter(borrow=_borrow_book).first() is not None:
                    return JsonResponse(data={
                        'status': 'error',
                        'msg': f'《{_borrow_book.book.book_name}》已经评价过了。'
                    })
                _borrow_comment = BorrowComment(borrow=_borrow_book, star=post['star'], comment=post['comment'])
                _borrow_comment.save()
            return JsonResponse(data={
                'status': 'success',
                'msg': '评价已提交。'
            })

    borrow_comment.layer = {
        # 弹出层中的输入框配置

        # 这里指定对话框的标题
        'title': '借书评价',
        # 提示信息
        'tips': '你对借书人的借书行为满意吗？给个评价吧。',
        # 确认按钮显示文本
        'confirm_button': '发布',
        # 取消按钮显示文本
        'cancel_button': '取消',

        # 弹出层对话框的宽度，默认50%
        'width': '40%',

        # 表单中 label的宽度，对应element-ui的 label-width，默认80px
        'labelWidth': "80px",
        'params': [
            {
                'type': 'rate',
                'key': 'star',
                'label': '等级'
            },
            {
                # 这里的type 对应el-input的原生input属性，默认为input
                'type': 'input',
                # key 对应post参数中的key
                'key': 'comment',
                # 显示的文本
                'label': '评价',
                # 为空校验，默认为False
                'require': True
            }
        ]
    }
    borrow_comment.short_description = '借书评价'
    borrow_comment.type = 'success'
    borrow_comment.icon = 'el-icon-s-promotion'

    actions = ['lend_book', 'return_book', 'borrow_comment']


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

    def return_book(self, request, queryset):
        # 这里的queryset 会有数据过滤，只包含选中的数据

        post = request.POST
        # 这里获取到数据后，可以做些业务处理
        # post中的_action 是方法名
        # post中 _selected 是选中的数据，逗号分割
        if not post.get('_selected'):
            return JsonResponse(data={
                'status': 'error',
                'msg': '请选择需要归还的书！'
            })
        else:
            for item in queryset:
                if item.status != 3:
                    return JsonResponse(data={
                        'status': 'error',
                        'msg': f'《{item.book.book_name}》状态无法归还，请重新选择。'
                    })
                else:
                    item.status = 4
                    item.save()
            return JsonResponse(data={
                'status': 'success',
                'msg': '申请成功，等待出借人确认图书已归还！'
            })

    return_book.short_description = '开始还书'
    return_book.type = 'success'
    return_book.icon = 'el-icon-s-promotion'

    return_book.layer = {
        # 弹出层中的输入框配置

        # 这里指定对话框的标题
        'title': '还书',
        # 提示信息
        'tips': '请和出借人商量好还书时间和地点。',
        # 确认按钮显示文本
        'confirm_button': '确认还书',
        # 取消按钮显示文本
        'cancel_button': '取消',

        # 弹出层对话框的宽度，默认50%
        'width': '40%',

        # 表单中 label的宽度，对应element-ui的 label-width，默认80px
        'labelWidth': "80px"
    }

    def borrow_book(self, request, queryset):
        # 这里的queryset 会有数据过滤，只包含选中的数据

        post = request.POST
        # 这里获取到数据后，可以做些业务处理
        # post中的_action 是方法名
        # post中 _selected 是选中的数据，逗号分割
        if not post.get('_selected'):
            return JsonResponse(data={
                'status': 'error',
                'msg': '请选择需要确认借阅的书！'
            })
        else:
            for item in queryset:
                if item.status != 2:
                    return JsonResponse(data={
                        'status': 'error',
                        'msg': f'《{item.book.book_name}》状态无法确认借书，请检查。'
                    })
                else:
                    item.status = 3
                    item.save()
            return JsonResponse(data={
                'status': 'success',
                'msg': f'申请成功，等待出借人确认图书已归还'
            })

    borrow_book.short_description = '确认借书'
    borrow_book.type = 'success'
    borrow_book.icon = 'el-icon-s-promotion'

    borrow_book.layer = {
        # 弹出层中的输入框配置

        # 这里指定对话框的标题
        'title': '确认借书',
        # 提示信息
        'tips': '收到书再进行确认，以保障自己的权益！',
        # 确认按钮显示文本
        'confirm_button': '我已收到书',
        # 取消按钮显示文本
        'cancel_button': '取消',

        # 弹出层对话框的宽度，默认50%
        'width': '40%',

        # 表单中 label的宽度，对应element-ui的 label-width，默认80px
        'labelWidth': "80px"
    }

    def lend_comment(self, request, queryset):
        # 这里的queryset 会有数据过滤，只包含选中的数据
        post = request.POST
        # 这里获取到数据后，可以做些业务处理
        # post中的_action 是方法名
        # post中 _selected 是选中的数据，逗号分割
        if not post.get('_selected'):
            return JsonResponse(data={
                'status': 'error',
                'msg': '选择需要评价的记录'
            })
        else:
            for _borrow_book in queryset:
                if _borrow_book.status != 5:
                    return JsonResponse(data={
                        'status': 'error',
                        'msg': f'《{_borrow_book.book.book_name}》需要等待出借人确认书已归还后才可评价。'
                    })
                elif LendComment.objects.filter(borrow=_borrow_book).first() is not None:
                    return JsonResponse(data={
                        'status': 'error',
                        'msg': f'《{_borrow_book.book.book_name}》已经评价过了。'
                    })
                _lend_comment = LendComment(borrow=_borrow_book, star=post['star'], comment=post['comment'])
                _lend_comment.save()
            return JsonResponse(data={
                'status': 'success',
                'msg': '评价已提交。'
            })

    lend_comment.layer = {
        # 弹出层中的输入框配置

        # 这里指定对话框的标题
        'title': '借书评价',
        # 提示信息
        'tips': '你对出借人借给你的书满意吗？给个评价吧。',
        # 确认按钮显示文本
        'confirm_button': '发布',
        # 取消按钮显示文本
        'cancel_button': '取消',

        # 弹出层对话框的宽度，默认50%
        'width': '40%',

        # 表单中 label的宽度，对应element-ui的 label-width，默认80px
        'labelWidth': "80px",
        'params': [
            {
                'type': 'rate',
                'key': 'star',
                'label': '等级'
            },
            {
                # 这里的type 对应el-input的原生input属性，默认为input
                'type': 'input',
                # key 对应post参数中的key
                'key': 'comment',
                # 显示的文本
                'label': '评价',
                # 为空校验，默认为False
                'require': True
            }
        ]
    }
    lend_comment.short_description = '借书评价'
    lend_comment.type = 'success'
    lend_comment.icon = 'el-icon-s-promotion'

    actions = ['borrow_book', 'return_book', 'lend_comment']


@admin.register(BorrowComment)
class BorrowCommentAdmin(AjaxAdmin):
    search_fields = ('comment', )
    list_display = ('borrow', 'lend_user', 'borrow_user', 'star', 'comment')
    list_per_page = 20

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def lend_user(self, obj):
        return obj.borrow.lend_user
    lend_user.short_description = "出借人"

    def borrow_user(self, obj):
        return obj.borrow.borrow_user
    borrow_user.short_description = "借书人"


@admin.register(LendComment)
class LendCommentAdmin(AjaxAdmin):
    search_fields = ('comment', )
    list_display = ('borrow', 'lend_user', 'borrow_user', 'star', 'comment')
    list_per_page = 20

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def lend_user(self, obj):
        return obj.borrow.lend_user
    lend_user.short_description = "出借人"

    def borrow_user(self, obj):
        return obj.borrow.borrow_user
    borrow_user.short_description = "借书人"
