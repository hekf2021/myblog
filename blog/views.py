from django.shortcuts import render_to_response,get_list_or_404,get_object_or_404
from .models import BlogType,Blog
from django.core.paginator import Paginator
# Create your views here.

def blog_list(request):
    page_num = request.GET.get('page',1)
    blog_all_list = Blog.objects.all()
    paginator =Paginator(blog_all_list,2)
    page_of_blogs=paginator.get_page(page_num)
    current_page_num = page_of_blogs.number #当前页
    page_range=list(range(max(current_page_num-2,1),current_page_num))+\
               list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1))

    context = {}
    context['page_of_blogs'] =page_of_blogs
    context['page_range'] = page_range
    context['blog_types']=BlogType.objects.all()
    return render_to_response('blog/blog_list.html', context)

def blog_detail(request,blog_pk):
    print(blog_pk)
    context = {}
    blog = get_list_or_404(Blog,pk=blog_pk)
    print(blog)
    context['blog']=blog[0]
    return render_to_response('blog/blog_detail.html', context)

def blog_with_type(request,blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blogs_with_type.html', context)