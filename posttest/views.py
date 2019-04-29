from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse

# Create your views here.
def index(request):
    return render(request,'posttest/index.html')

#显示登陆界面
def login(request):
    return render(request,'posttest/login.html')

def login_check(request):
    #return HttpResponse('ok')
    #获取用户名称和密码
    user_name=request.GET.get('username')
    password=request.GET.get('password')

    if user_name=='p' and password=='1':
        return redirect('/index')
    else:
        return redirect('/login')

def ajax_login(request):
    return render(request,'posttest/ajax_login.html')

def ajax_login_check(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username =='jx' and password=='123':
        return JsonResponse({'res':1})
        #return redirect('/index') Ajax必须返回Json，让js处理，不然浏览器还是停留在该页面，
    else:
        return JsonResponse({'res':0})



