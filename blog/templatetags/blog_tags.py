import bleach
from django import template
from django.utils.safestring import mark_safe
from blog.models import Post,Category
from django.utils import timezone
from taggit.models import Tag

register = template.Library()

ALLOWED_TAGS = [
    'p','br','hr','div','span','h1','h2','h3','h4','h5','h6',
    'strong','b','em','i','u','s','blockquote','code','pre',
    'ul','ol','li','a','img','table','thead','tbody','tr','th','td',
    'figure','figcaption',
]
ALLOWED_ATTRIBUTES = {
    '*': ['class'],
    'a': ['href','title','target','rel'],
    'img': ['src','alt','title','width','height'],
}


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

@register.filter
def clean_html(value):
    return mark_safe(bleach.clean(value or '', tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True))



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


@register.inclusion_tag('blog/blog-tags.html')
def alltags():
    tags = Tag.objects.all().order_by('name')
    return {'tags': tags}


@register.inclusion_tag('blog/home-latest-posts.html')
def home_latest_posts(arg=3):

    posts = Post.objects.filter(
        published_date__lte=timezone.now(),
        status=True
    ).order_by('-published_date')[:arg]

    return {
        'posts': posts
    }