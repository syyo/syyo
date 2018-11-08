from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator,Page
from haystack.generic_views import SearchView
# Create your views here.


def index(request):
    '''
    数据结构：分类对象，最新的4个，最火的3个
    {type:,new:,click:}
    [{},{},{},{},{},{}]
    '''
    # 查询所有的分类
    type_list = TypeInfo.objects.all()
    list = []
    for type in type_list:
        # 查询最新的4个商品
        new = type.goodsinfo_set.all().order_by('-id')[0:4]
        # 查询点击量最高的3个商品
        click = type.goodsinfo_set.all().order_by('-gclick')[0:3]
        # 构造数据提供给模板
        list.append({'type': type, 'new': new, 'click': click})
    context = {'title': '首页', 'iscart': 1, 'list': list}
    return render(request, 'tt_goods/index.html', context)


def list(request, tid, pindex, porder):
    # 查询当前分类的名称
    type_title = TypeInfo.objects.get(id=tid).ttitle
    # 查询当前分类最新的两个商品
    gnew = GoodsInfo.objects.filter(gtype_id=tid).order_by('-id')[0:2]
    # 按照指定反序规则进行查询
    order_str = '-id'
    if porder == '2':
        order_str = '-gprice'
    elif porder == '3':
        order_str = '-gclick'
    glist = GoodsInfo.objects.filter(gtype_id=tid).order_by(order_str)
    # 分页显示数据
    paginator = Paginator(glist, 10)
    pindex1 = int(pindex)
    page = paginator.page(pindex1)
    # 构造上下文传递给模板
    context = {'title': '商品列表', 'iscart': 1, 'page': page, 'new': gnew, 'tid': tid, 'pindex': pindex1, 'order': porder, 'type_title': type_title}
    return render(request, 'tt_goods/list.html', context)


def detail(request, gid):
    # 查询当前商品
    goods = GoodsInfo.objects.get(id=gid)
    # 让点击量加1
    goods.gclick += 1
    goods.save()
    # 查询当前商品对应分类的最新的两个商品
    new = goods.gtype.goodsinfo_set.all().order_by('-id')[0:2]

    context = {'title': '商品详情', 'iscart': 1, 'goods': goods, 'new': new}
    response = render(request, 'tt_goods/detail.html', context)
    # 加入最近浏览 '1,2,3,4,5'
    gid = str(goods.id)
    zjll = request.COOKIES.get('zjll', '')
    zjll_list = [gid]
    if zjll:
        zjll_list = zjll.split(',')
        # 如果列表中已经存在当前商品
        if gid in zjll_list:
            zjll_list.remove(gid)
        # 将当前商品加到第一个
        zjll_list.insert(0, gid)
        # 控制个数，保持在5个
        if len(zjll_list) > 5:
            zjll_list.pop()

    response.set_cookie('zjll', ','.join(zjll_list), expires=60*60*24*7)

    return response


class GoodsSearchView(SearchView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['iscart'] = 1
        context['qwjs'] = 2
        return context

