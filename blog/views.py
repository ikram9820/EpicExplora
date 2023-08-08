from django.shortcuts import render,get_object_or_404,get_list_or_404
from .models import *
# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    return render(request,"blog/post/list.html",{'posts': posts})

def post_detail(request,pk):
    post = get_object_or_404(Post,id=pk,status=Post.Status.PUBLISHED)
    return render(request,"blog/post/detail.html",{'post':post})