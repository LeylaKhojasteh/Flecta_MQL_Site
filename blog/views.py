from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post,Comment
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.forms import CommentForm
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect


# Create your views here.
def blog_view(request,**kwargs):
    posts = Post.objects.filter(status=True,published_date__lte=timezone.now()).order_by('-published_date')
    if kwargs.get('cat_name') != None:
        posts = posts.filter(category__name=kwargs['cat_name'])
    if kwargs.get('author_username') != None:
        posts = posts.filter(author__username=kwargs['author_username']) 
    if kwargs.get('tag_name') != None:
        posts = posts.filter(tags__name__in=[kwargs['tag_name']]) 

    posts = Paginator(posts,4)  
    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except EmptyPage:
        posts = posts.get_page(1)
    except PageNotAnInteger:
        posts = posts.get_page(1)

    context = {'posts':posts}
    return render(request,'blog/blog-home.html',context)
    

def blog_single(request,pid):
    post = get_object_or_404(Post,id=pid, status=True, published_date__lte=timezone.now())
    if post.login_require and not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:login'))

    if request.method == "GET":
        post.counted_views += 1
        post.save(update_fields=['counted_views'])

    if request.method == "POST":
        form = CommentForm(request.POST, user=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.name = request.user.username
                comment.email = request.user.email
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Your comment has submitted successfully!')
            return redirect('blog:single', pid=post.id)
        else:
            messages.add_message(request,messages.ERROR,'Your comment was not submitted. Please check the form.')
    else:
        form = CommentForm(user=request.user)

    posts = list(Post.objects.filter(status=True,published_date__lte=timezone.now()).order_by('-published_date'))
    comments = Comment.objects.filter(post=post.id,approved=True)
    prv_post = None
    nxt_post = None
    index = posts.index(post)
    if (index>0):
        prv_post = posts[index-1]
    if(index < len(posts)-1):
        nxt_post = posts[index+1]

    context = {'post':post,'prv':prv_post,'nxt':nxt_post,'comments':comments,'form':form}

    return render(request,'blog/blog-single.html',context)

def blog_category(request,cat_name):
    posts = Post.objects.filter(status=True)
    posts = posts.filter(category__name=cat_name)
    context = {'posts':posts}
    return render(request,'blog/blog-home.html',context)



def blog_search(request):
    posts = Post.objects.filter(status=True)
    if request.method == 'GET':
        if s:= request.GET.get('s'):
            posts = posts.filter(content__contains=s)  

    context = {'posts':posts}
    return render(request,'blog/blog-home.html',context)


