from django import template
from blog.models import Post,Category
from django.utils import timezone

register = template.Library()


@register.simple_tag(name='totalposts')
def function():
    posts = Post.objects.filter(status=True).count()
    return posts

@register.simple_tag(name='posts')
def function():
    posts = Post.objects.filter(status=True)
    return posts



@register.filter
def snippet(value,arg=20):
    return value[:arg]+'...'



@register.inclusion_tag('blog/blog-latest-posts.html')
def latestposts(arg=4):
    posts = Post.objects.filter(published_date__lte=timezone.now(),status=True).order_by("-published_date")[:arg]
    return {"posts":posts}


@register.inclusion_tag('blog/blog-post-categories.html')
def postcategories():
    posts = Post.objects.filter(published_date__lte=timezone.now(),status=True)
    categories = Category.objects.all()
    cat_dict = {}
    for name in categories:
        cat_dict[name] = posts.filter(category=name).count()
    return {"categories":cat_dict}


@register.inclusion_tag('blog/recent-blog-posts.html')
def recentblogposts(arg=6):
    posts = Post.objects.filter(published_date__lte=timezone.now(),status=True).order_by("-published_date")[:arg]
    return {"posts":posts}