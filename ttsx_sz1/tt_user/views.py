# coding=utf-8
from django.shortcuts import render, redirect
from .models import *
from hashlib import sha1
from django.http import HttpResponse, JsonResponse
from . import task
from .user_decorators import *
from PIL import Image, ImageDraw, ImageFont
from tt_goods.models import *
from tt_order.models import *
from django.core.paginator import Paginator, Page


def register(request):
    # 显示注册页面
    return render(request, 'tt_user/register.html')


def register_handle(request):
    # 接收请求的数据：用户名、密码、邮箱
    dict = request.POST
    uname = dict.get('user_name')
    upwd = dict.get('pwd')
    uemail = dict.get('email')

    # 对密码进行sha1加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd_sha1 = s1.hexdigest()

    # 将数据存入表中，使用模型类
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd_sha1
    user.uemail = uemail
    user.save()

    # 向注册邮箱中发送邮件，进行激活
    # msg='<a href="http://127.0.0.1:8000/user/active%s/">点击激活</a>'%(user.id)
    # send_mail('天天生鲜用户激活','',settings.EMAIL_FROM,[uemail],html_message=msg)
    # 调用celery里定义的sendmail函数的delay()方法，发送邮件
    task.sendmail.delay(user.id, uemail)

    return HttpResponse('用户账册成功，请到邮箱中激活')

'''
通过邮箱的链接，激活刚注册的账户
'''


def active(request, uid):
    # 通过url带的id查询一个user对象
    user = UserInfo.objects.get(id=uid)
    # 修改isActive属性，激活
    user.isActive = True
    user.save()

    return HttpResponse('激活成功，<a href="/user/login/">点击登录</a>')


def say_hello(request):
    # print('hello...')
    # time.sleep(2)
    # print('django...')
    # 将任务加入到队列中
    task.sayhello.delay()
    # 返回响应
    return HttpResponse('ok')


@is_login
def center(request):
    # 判断是否登录
    # if 'uid' in request.session:
    #     context={'title':'用户中心'}
    #     return render(request,'tt_user/user_center_info.html',context)
    # else:
    #     return redirect('/user/login/')

    # 读取最近浏览信息
    zjll = request.COOKIES.get('zjll')
    goods_list = []
    if zjll:
        zjll_list = zjll.split(',')
        for gid in zjll_list:
            goods_list.append(GoodsInfo.objects.get(id=gid))
    context = {'title': '用户中心', 'goods_list': goods_list}
    return render(request,'tt_user/user_center_info.html', context)


@is_login
def order(request):
    # 订单表
    pindex = request.GET.get('page', '1')
    # 获取session里的用户id
    uid = request.session.get('uid')
    # 通过用户id去查订单表
    orders = OrderInfo.objects.filter(user_id=uid).order_by('-odate')
    # 把订单报表分页显示，每页2条信息
    paginator = Paginator(orders, 2)

    page = paginator.page(int(pindex))
    context = {'title': '我的订单', 'page': page}
    return render(request, 'tt_user/user_center_order.html', context)


@is_login
def site(request):
    # 地址表
    uid = request.session.get('uid')
    # 通过用户id去查地址表
    sites = UserAddressInfo.objects.filter(user_id=uid)
    site = UserAddressInfo()
    # 获取模板里的site_id
    sid = request.GET.get('sid')
    if sid:
        # 通过sid获取地址对象
        site = UserAddressInfo.objects.get(id=sid)
    context = {'title': '收货地址', 'sites': sites, 'site': site}
    return render(request, 'tt_user/user_center_site.html', context)


@is_login
def site_handle(request):
    # 地址表请求处理
    dict = request.POST
    # 获取session里的uid
    uid = request.session.get('uid')
    # 获取模板里的表单属性
    sid = dict.get('sid')
    uname = dict.get('uname')
    uaddress = dict.get('uaddress')
    uphone = dict.get('uphone')

    if sid == '0':  # 新增
        address = UserAddressInfo()
    else:  # 修改
        address = UserAddressInfo.objects.get(id=sid)

    address.uname = uname
    address.uphone = uphone
    address.uaddress = uaddress
    address.user_id = uid
    address.save()

    return redirect('/user/site/')


def register_name(request):
    # 验证是否有账号
    # 获取模板里的uname
    uname = request.GET.get('uname')
    # 去数据库查询uname的数量
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    # 登录页面
    # 获取cookie的uname，默认返回空字符串
    uname = request.COOKIES.get('user_name', '')
    context = {'title': '登录', 'uname': uname}
    return render(request, 'tt_user/login.html', context)


def login_handle(request):
    # 判断是否为post请求
    if request.method == "GET":
        return redirect('/user/login/')
    # 接收请求的用户名、密码
    dict = request.POST
    uname = dict.get('username')
    upwd = dict.get('pwd')
    urem = dict.get('remember', '0')
    yzm = dict.get('yzm')
    # 定义返回的上下文
    context = {'title': '登录', 'uname': uname, 'upwd': upwd, 'uname_error': 0, 'upwd_error': 0}

    # 判断验证码是否正确
    # if yzm!=request.session['verifycode']:
    #     return render(request, 'tt_user/login.html', context)
    # 根据用户名查询数据
    user = UserInfo.objects.filter(uname=uname)
    if user:
        # 用户名存在
        upwd_db = user[0].upwd
        # 对密码加密
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        upwd_sha1 = s1.hexdigest()
        # 对比密码
        if upwd_db == upwd_sha1:
            # 密码正确
            # 判断是否激活
            if user[0].isActive:
                # 登录成功
                response = redirect(request.session.get('url_path', '/'))
                # HttpResponseRedirect HttpResponse
                # 记住用户名
                if urem == '1':
                    response.set_cookie('user_name', uname, expires=60*60*24*14)
                else:
                    response.set_cookie('user_name', '', expires=-1)
                request.session['uid'] = user[0].id
                request.session['uname'] = uname
                return response
            else:
                return HttpResponse('账户未激活，请先到邮箱中激活再登录')
        else:
            #  密码错误
            context['upwd_error'] = 1
            return render(request, 'tt_user/login.html', context)

    else:
        # 用户名不存在
        context['uname_error'] = 1
        return render(request, 'tt_user/login.html', context)


def logout(request):
    # 退出清除session数据
    request.session.flush()
    return redirect('/')


def verify_code(request):
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str

    # 内存文件操作(python2)
    # import cStringIO
    # buf = cStringIO.StringIO()

    # 内存文件操作(python3)
    from io import BytesIO
    buf = BytesIO()

    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


