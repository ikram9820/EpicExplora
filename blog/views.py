from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector,SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Count
from django.shortcuts import render,get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .models import Post
from .forms import CommentForm, EmailPostForm, SearchForm
from taggit.models import Tag

# class PostListView(ListView):
    # queryset = Post.published.all()
    # context_object_name = 'posts'
    # paginate_by = 3
    # template_name = 'blog/post/list.html'

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
    
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_query = SearchQuery(query)
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            results = Post.published.annotate(search=search_vector,rank=SearchRank(search_vector, search_query))\
                          .filter(rank__gte=0.3).order_by('-rank')
            # results = Post.published.filter(title__icontains = query)
            # results = Post.published.annotate(similarity=TrigramSimilarity('title', query),).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request,'blog/post/search.html', {'form': form,'query': query,'results': results})