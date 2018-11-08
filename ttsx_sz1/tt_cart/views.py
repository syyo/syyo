from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from tt_user.user_decorators import *
from django.db.models import Sum
# Create your views here.
@is_login
def index(request):
    uid=request.session.get('uid')
    cart_list=CartInfo.objects.filter(user_id=uid)#request.session['uid']
    context={'clist':cart_list,'title':'购物车'}
    return render(request,'tt_cart/cart.html',context)

'''
http://127.0.0.1:8000/order/?cid=1&cid=3

'''

@is_login
def add(request):
    uid=request.session.get('uid')
    #接收请求的商品和数量
    dict=request.GET
    gid=int(dict.get('gid'))
    count=int(dict.get('count'))
    #判断当前用户是否已经将此商品加入购物车
    carts=CartInfo.objects.filter(user_id=uid,goods_id=gid)
    if carts:#如果已经加入则修改数量
        cart=carts[0]
        cart.count+=count
        cart.save()
    else:#如果未加入则新建
        cart=CartInfo()
        cart.user_id=uid
        cart.goods_id=gid
        cart.count=count
        cart.save()

    if request.is_ajax():
        # c = CartInfo.objects.filter(user_id=request.session.get('uid')).count()
        c=CartInfo.objects.filter(user_id=request.session.get('uid')).aggregate(Sum('count'))
        return JsonResponse({'ok':1,'count':c.get('count__sum')})
    else:
        return redirect('/cart/')

def edit(request):
    dict=request.GET
    cid=int(dict.get('cid'))
    count=int(dict.get('count'))

    #查询购物车并修改
    cart=CartInfo.objects.get(id=cid)
    cart.count=count
    cart.save()

    return JsonResponse({'ok':1})

def remove(request):
    cid=request.GET.get('cid')
    cart=CartInfo.objects.get(id=cid)
    cart.delete()
    return JsonResponse({'ok':1})

def count(request):
    c=CartInfo.objects.filter(user_id=request.session.get('uid')).count()
    return JsonResponse({'count':c})