from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
# Create your views here.

def post_list(request):
    posts = Post.published.all()
    POST_PER_PAGE = 2
    PAGE_NO = request.GET.get('page', 1)
    paginator = Paginator(posts,POST_PER_PAGE)
    try:
        posts = paginator.page(PAGE_NO)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,"blog/post/list.html",{'posts': posts})

def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post,publish__year=year,publish__month=month,
                             publish__day=day,status=Post.Status.PUBLISHED)
    return render(request,"blog/post/detail.html",{'post':post}) 