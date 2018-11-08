from django.shortcuts import redirect
from django.http import JsonResponse,HttpRequest


def is_login(fn):
    # 装饰器，验证登录状态
    def fun(request, *args, **kwargs):
        # 判断是否登录
        if 'uid' in request.session:
            return fn(request, *args, **kwargs)
        else:
            # 如果当前是ajax请求，则返回json，否则告诉浏览器跳转
            if request.is_ajax():
                return JsonResponse({'login':1})
            else:
                return redirect('/user/login/')
    return fun

