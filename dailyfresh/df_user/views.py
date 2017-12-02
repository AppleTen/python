from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse,JsonResponse
from df_user.models import Passport
from celery_tasks.tasks import send_active_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
import re


def register(request):
    '''显示用户注册页面'''
    return render(request, 'df_user/register.html')


def register_handle(request):
    '''进行用户注册处理'''
    # 接收数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')

    # 进行数据校验
    if not all([username, password, email]):
        # 有数据为空
        return render(request, 'df_user/register.html', {'errmsg':'参数不能为空!'})

    # 判断邮箱是否合法
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        # 邮箱不合法
        return render(request, 'df_user/register.html', {'errmsg':'邮箱不合法!'})

    # 进行业务处理:注册
    # Passport.objects.create(username=username, password=password, email=email)
    passport = Passport.objects.add_one_passport(username=username, password=password, email=email)

    # 生成激活的token
    serializer = Serializer(settings.SECRET_KEY, 3600)
    token = serializer.dumps({'confirm':passport.id}) # 返回bytes
    token = token.decode()

    # 给用户的邮箱发激活邮件
    # send_mail('天天生鲜用户激活', '', settings.EMAIL_FROM, [email], html_message='<a href="www.baidu.com">百度</a>')
    send_active_email.delay(token, username, email)

    # 返回应答，跳转的首页
    return redirect(reverse('goods:index'))


def register_active(request, token):
    '''用户账户激活'''
    serializer = Serializer(settings.SECRET_KEY, 3600)
    try:
        info = serializer.loads(token)
        passport_id = info['confirm']
        # 进行用户激活
        passport = Passport.objects.get(id=passport_id)
        passport.is_active = True
        passport.save()
        # 跳转的登录页
        return redirect(reverse('user:login'))
    except SignatureExpired:
        # 链接过期
        return HttpResponse('激活链接已过期')


def check_user_exist(request):
    '''校验用户名是否存在'''
    # 1.接收数据
    username = request.GET.get('username')

    # 2.根据用户名查找账户信息
    try:
        Passport.objects.get(username=username)
        return JsonResponse({'res':0})
    except Passport.DoesNotExist:
        # 用户名可用
        return JsonResponse({'res':1})


def login(request):
    '''显示登录页面'''
    return render(request, 'df_user/login.html')
