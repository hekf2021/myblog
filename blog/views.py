from django.shortcuts import render_to_response,get_list_or_404,get_object_or_404
from .models import BlogType,Blog
from django.core.paginator import Paginator
from django.db.models import  Count
from read_statistics.utils import read_statistics_once_read
# Create your views here.

def blog_detail(request,blog_pk):
    context = {}
    blog = get_object_or_404(Blog,pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request,blog)

    context['blog']=blog
    context['previous_blog']=Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['next_blog']=Blog.objects.filter(create_time__lt=blog.create_time).first()
    response = render_to_response('blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key,'true');
    return response

def blog_with_type(request,blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blogs_with_type.html', context)


def get_blog_list_common_data(blog_all_list,page_num):
    paginator = Paginator(blog_all_list, 5)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number  # 当前页
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))


    '''
    统计blog_type类型数量
    方法一：
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)
    方法二：
    BlogType.objects.annotate(blog_count=Count('blog'))  #统计blog_type的数量，返回给页时，blog_types是数组，里面装的对象是blog_type，另外给blog_type加了一个blog_count的属性
    '''

    '''
    统计日期数有多少博客
    方法一
    blog_dates_dict = {}
    blog_dates =Blog.objects.dates('create_time', 'month', order='DESC')
    for blog_date in blog_dates:
        blog_count=Blog.objects.filter(create_time__year=blog_date.year,create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date]=blog_count
    '''
    blog_dates_dict = {}
    blog_dates = Blog.objects.dates('create_time', 'month', order='DESC')
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year, create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))  #统计blog_type的数量，返回给页时，blog_types是数组，里面装的对象是blog_type，另外给blog_type加了一个blog_count的属性
    context['blog_dates'] = blog_dates_dict
    return context


def blog_list(request):
    page_num = request.GET.get('page',1)
    blog_all_list = Blog.objects.all()
    context = get_blog_list_common_data(blog_all_list,page_num)
    return render_to_response('blog/blog_list.html', context)

def blog_with_date(request,year,month):
    page_num = request.GET.get('page', 1)
    blog_all_list = Blog.objects.filter(create_time__year=year,create_time__month=month)
    context = get_blog_list_common_data(blog_all_list,page_num)
    context['blogs_with_data'] = '%s年%s月' % (year,month)
    return render_to_response('blog/blogs_with_date.html', context)