from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post
import markdown

# Create your views here.
def index(request):
    #return HttpResponse('hello,this is my 博客首页')
    #return render(request,'index.html',context={'title':'first love','welcome':'*zhang'})
    post_list=Post.objects.all().order_by('create_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

def detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.body=markdown.markdown(post.body,extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    return render(request,'blog/detail.html',context={'post':post})
