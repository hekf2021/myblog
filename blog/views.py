from django.shortcuts import render_to_response,get_list_or_404,get_object_or_404
from .models import BlogType,Blog
# Create your views here.

def blog_list(request):
    context = {}
    context['blogs'] = Blog.objects.all()
    context['blog_count']=Blog.objects.all().count()
    return render_to_response('blog/blog_list.html',context)

def blog_detail(request,blog_pk):
    print(blog_pk)
    context = {}
    blog = get_list_or_404(Blog,pk=blog_pk)
    print(blog)
    context['blog']=blog[0]
    return render_to_response('blog/blog_detail.html',context)

def blog_with_type(request,blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    return render_to_response('blog/blogs_with_type.html',context)