from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.postgres.search import SearchVector,SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.forms import ValidationError
from django.shortcuts import redirect, render,get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils.text import slugify
from taggit.models import Tag
from .models import Post
from .forms import CommentForm, EmailPostForm, SearchForm, EditPostForm,AddPostForm

def post_list(request,tag_slug=None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    POST_PER_PAGE = 5
    PAGE_NO = request.GET.get('page', 1)
    paginator = Paginator(posts,POST_PER_PAGE)
    try:
        posts = paginator.page(PAGE_NO)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,"blog/post/list.html",{'posts': posts,"tag":tag})

def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post,publish__year=year,publish__month=month,
                             publish__day=day,status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    form = CommentForm()
    return render(request,"blog/post/detail.html",{'post':post,'comments': comments,'form': form,
                                                   'similar_posts': similar_posts}) 
@login_required
def add_post(request):
    if request.method == 'POST':
        post_form = AddPostForm(data = request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.tags.add(*post_form["tags"].value().split(","))
            post.save()

            url = reverse('dashboard')
            return redirect(url)
        
    else:
        post_form = AddPostForm()
    return render(request, 'blog/post/add.html',{"post_form":post_form})

@login_required
def edit_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        if request.user != post.author:
            messages.error(request,"you are not allowed to edit this post")
            post_form = EditPostForm(instance=post)

        else:
            post_form = EditPostForm(instance=post,data = request.POST)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.slug = slugify(post.title)
                post.tags.add(*post_form["tags"].value().split(","))
                post.save()
                return redirect(post.get_absolute_url())
        
    else:
        post_form = EditPostForm(instance=post)
    return render(request, 'blog/post/edit.html',{"post_form":post_form})


@login_required
def delete_post(request,pk):
    post = get_object_or_404(Post, pk=pk)

    post.delete()
    url = reverse("dashboard")
    return redirect(url)
@login_required  
def delete_confirm(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request,"you are not allowed to delete this post")
        return redirect(post.get_absolute_url())
    return render(request, "blog/post/delete_confirm.html",{"post":post})



@login_required
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
        return redirect(post.get_absolute_url())
    
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # results = Post.published.filter(title__icontains = query)
            results = Post.published.annotate(similarity=TrigramSimilarity('title', query),).filter(similarity__gt=0.1).order_by('-similarity')
            # search_query = SearchQuery(query)
            # search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            # results = Post.published.annotate(search=search_vector,rank=SearchRank(search_vector, search_query))\
            #               .filter(rank__gte=0.3).order_by('-rank')
            
    return render(request,'blog/post/search.html', {'form': form,'query': query,'results': results})