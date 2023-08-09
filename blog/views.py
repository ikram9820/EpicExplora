from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from .models import Post
from .forms import CommentForm, EmailPostForm

# class PostListView(ListView):
    # queryset = Post.published.all()
    # context_object_name = 'posts'
    # paginate_by = 3
    # template_name = 'blog/post/list.html'

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
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request,"blog/post/detail.html",{'post':post,'comments': comments,'form': form}) 

def share_post(request,id):
    post = get_object_or_404(Post, pk=id)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you to read {post.title}"
            message = f"read {post.title} at {post_url} \n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject,message,"ikram9820khan@gmail.com",[cd["to"]])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, "blog/post/share.html",{"form": form,"post":post,"sent":sent})


@require_POST
def post_comment(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return render(request, 'blog/post/comment.html',{'post': post,'form': form,'comment': comment})