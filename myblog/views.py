import datetime
from django.utils import timezone
from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data,get_today_hot_data,get_yesterday_hot_data
from blog.models import Blog
from django.db.models import Sum
from django.core.cache import cache
from django.contrib import auth
from django.urls import reverse

def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
        .filter(read_details__date__lt=today,read_details__date__gte=date) \
        .values('id','title') \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return blogs[:7]

def home(request):
    blog_content_type= ContentType.objects.get_for_model(Blog)
    dates,read_nums=get_seven_days_read_data(blog_content_type)

    #获取7天热门博客的缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days=get_7_days_hot_blogs
        cache.set('hot_blogs_for_7_days',hot_blogs_for_7_days,3600)
        print('计算')
    else:
        print('使用缓存..')

    context= { }
    context['read_nums']=read_nums
    context['dates'] = dates
    context['today_host_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_host_data'] = get_yesterday_hot_data(blog_content_type)
    context['hot_blogs_for_7_days'] = hot_blogs_for_7_days
    return render(request,'home.html',context)

def login(request):
    username = request.POST.get('username','')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    referer=request.META.get('HTTP_REFERER',reverse('home')) #请求过来的页面网址
    if user is not None:
        auth.login(request, user)
        return redirect(referer) #跳回到原来的页面
    else:
        return render(request,'error.html',{'message':'用户名或密码不正确',"redirect_to":referer})