from django.shortcuts import render,redirect,HttpResponse
from apps.user.models import User#引用绝对地址以免报错
from django.views.generic import View

from django.core.mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from itsdangerous import SignatureExpired
from celery_tasks.tasks import send_register_active_email


# Create your views here.
def register(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        if not all([username, password, email]):
            return render(request, 'register.html', context={'errmsg': '数据不完整'})
        # 进行业务处理，用户注册保存在数据库
        try:
            user_re = User.objects.get(username=username)
        except User.DoesNotExist:
            user_re = None
        if user_re:
            return render(request, 'register.html', context={'errmsg': '用户名已存在'})
        user = User()
        user.username = username
        user.password = password
        user.email = email
        user.is_active = 0
        user.save()
        # django内置的模块保存数据库与上述操作一样
        # user=User.objects.create_user(username,password,email)
        return redirect('goods:index')


def register_handle(request):
    username=request.POST.get('user_name')
    password=request.POST.get('pwd')
    email=request.POST.get('email')
    if not all([username,password,email]):
        return render(request,'register.html',context={'errmsg':'数据不完整'})
    #进行业务处理，用户注册保存在数据库
    try:
        user_re=User.objects.get(username=username)
    except User.DoesNotExist:
        user_re=None
    if user_re:
        return render(request,'register.html',context={'errmsg':'用户名已存在'})
    user=User()
    user.username=username
    user.password=password
    user.email=email
    user.is_active=0
    user.save()
    #django内置的模块保存数据库与上述操作一样
    #user=User.objects.create_user(username,password,email)
    return redirect('goods:index')

#注册类
class RegisterView(View):
    def get(self,request):
        return render(request, 'register.html')

    def post(self,request):
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        if not all([username, password, email]):
            return render(request, 'register.html', context={'errmsg': '数据不完整'})
        # 进行业务处理，用户注册保存在数据库
        try:
            user_re = User.objects.get(username=username)
        except User.DoesNotExist:
            user_re = None
        if user_re:
            return render(request, 'register.html', context={'errmsg': '用户名已存在'})
        #进行用户注册
        user = User()
        user.username = username
        user.password = password
        user.email = email
        user.is_active = 0
        user.save()
        # django内置的模块保存数据库与上述操作一样
        # user=User.objects.create_user(username,password,email)

        #用户激活,参数依次为加密方式和过期时间
        serializer=Serializer(settings.SECRET_KEY,3600)
        info={'confirm':user.id}
        token=serializer.dumps(info)
        token = token.decode('utf8')  # 解码, str
        # #邮箱激活
        # subject = '天天生鲜欢迎信息'
        # message = ''
        # sender = settings.EMAIL_FROM  # 发送人
        # receiver = [email]
        # html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员' \
        #                '</h1>请点击下面链接激活您的账户<br/>' \
        #                '<a href="http://127.0.0.1:8000/user/active/%s">' \
        #                'http://127.0.0.1:8000/user/active/%s' \
        #                '</a>' % (username, token, token)
        #
        # send_mail(subject, message, sender, receiver, html_message=html_message)
        #验证

        #使用celery异步执行任务
        send_register_active_email.delay(email,username,token)
        return redirect('goods:index')

class ActiveView(View):
    def get(self,request,token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            #解密
            info=serializer.loads(token)
            #获取用户id
            user_id=info['confirm']
            user=User.objects.get(id=user_id)
            user.is_active=1
            user.save()
            #跳转到登陆页面
            return redirect('user:login')
        except SignatureExpired as e:
            return HttpResponse('激活过期')


class LoginView(View):
    def get(self,request):
        return render(request,'login.html')