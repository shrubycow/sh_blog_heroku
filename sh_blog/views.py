from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.views.generic.base import TemplateView
from .models import Post, Rubric, TodaySchedule, Comment, UserProfile
from precise_bbcode.bbcode import get_parser
from .forms import CommentForm
import datetime
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

# Create your views here.

def bb_parse(elements):
    parser = get_parser()
    try:
        iter(elements)
        for element in elements:
            element.body = parser.render(str(element.body))
    except TypeError:
        elements.body = parser.render(str(elements.body))
    return elements

def test(request):
    response  = HttpResponse('Hello moto')
    response.delete_cookie('not_first_time')
    return response

def index(request):
    if 'not_first_time' in request.COOKIES:
        posts = Post.objects.order_by('-created').filter(status='published')[:5]
        posts = bb_parse(posts)
        schedule = TodaySchedule.objects.all()
        response = render(request, 'sh_blog/index.html', {'posts': posts, 'schedule': schedule})
    else:
        template = get_template('sh_blog/greetings.html')
        response = HttpResponse(template.render(request=request))
        expires = datetime.datetime(year=9999, month=1, day=1)
        response.set_cookie('not_first_time', True, expires=expires)
    return response

def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    post = bb_parse(post)
    comments = Comment.objects.filter(post__slug=slug)
    if request.method == 'POST':
        if request.user.is_authenticated:    
            form = CommentForm(request.POST)
            if form.is_valid:
                new_comment = form.save(commit=False)
                new_comment.post = Post.objects.get(slug=slug)
                new_comment.profile = UserProfile.objects.get(user=request.user)
                new_comment = bb_parse(new_comment)
                new_comment.save()
                return redirect('sh_blog:detail', slug)
            return render(request, 'sh_blog/detail.html', {'post': post, 'comments': comments, 'form': form})
        else:
            raise PermissionDenied
    else:
        form = CommentForm()
        return render(request, 'sh_blog/detail.html', {'post': post, 'comments': comments, 'form': form})


def not_about_work(request):
    rubrics = Rubric.objects.exclude(name='Сайт').exclude(name='Работа')
    return render(request, 'sh_blog/not_work.html', {'rubrics': rubrics})

def by_rubric(request, pk):
    posts = Post.objects.filter(rubric__id=pk).filter(status='published')
    posts = bb_parse(posts)
    rubric = Rubric.objects.get(id=pk)
    return render(request, 'sh_blog/by_rubric.html', {'posts': posts, 'rubric': rubric})


    