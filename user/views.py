from textwrap import fill
from django.http import JsonResponse
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from .models import User, Follow
import hashlib
from msg.views import check_login
from PIL import Image, ImageFont, ImageDraw
from random import randint
import random
# 把文件以byte格式存在内存中
from io import BytesIO
from plate.models import Plate
from msg.models import Article, Comment
from django.db import connection


# Create your views here.

# 注册
def register(request):
    if request.method == 'GET':
        text = request.GET.get('text')
        return render(request, 'register1.html', locals())

    elif request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
    # 比较两次密码是否一致
        if password1 != password2:
            text = '两次输入的密码不一致'
        # href = '/user/reguist'
            return HttpResponseRedirect('/user/register?text={}'.format(text))
        # return render(request, 'error.html', locals())
    # 验证当前用户名是否存在
        user = User.objects.filter(name = username)
        if user:
            text = '用户名已存在'
            return HttpResponseRedirect('/user/register?text={}'.format(text))
    # 密码加密
        m = hashlib.md5()
        m.update(password1.encode()) # 修改指定编码为utf-8
        passwordm = m.hexdigest()  # 修改为十六进制
    # 插入数据
        try:
            use = User.objects.create(name = username, password = passwordm)
            file_obj = request.FILES.get('file')
            print(file_obj)
            filename='./static/images/user_images/'+str(use.uid) + '.jpg'
            if file_obj.name.split('.')[-1] not in ['jpeg','jpg','png']:
                return HttpResponse('输入文件有误')
            with open(filename,'wb+') as f:
                f.write(file_obj.read())
        except Exception as e:
            print('user create is error %s' % e)
            text = '头像未上传'
            return HttpResponseRedirect('/user/register?text={}'.format(text))
    # 免登录一天 
        request.session['username'] = username
        request.session['uid'] = use.uid
        resp = HttpResponseRedirect('/home')
        resp.set_cookie('username', username, 3600 * 24)
        resp.set_cookie('uid', use.uid, 3600 * 24)
        return resp

    elif request.is_ajax():
        response = {'code':100,'msg':None}
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        file = request.POST.get('file')
        print(file)
        print(username)
        print(password1)
        print(password2)
        if password1 != password2:
            response['code'] = 102
            response['msg'] = '两次输入的密码不一致'
        elif User.objects.filter(name = username):
            response['code'] = 103
            response['msg'] = '用户名已存在'
        else:
            # 密码加密
            m = hashlib.md5()
            m.update(password1.encode()) # 修改指定编码为utf-8
            passwordm = m.hexdigest()  # 修改为十六进制
            # 插入数据
            try:
                use = User.objects.create(name = username, password = passwordm)
                request.session['username'] = username
                request.session['uid'] = use.uid
                response['uid'] = use.uid
            except:
                response['code'] = 103
                response['msg'] = '用户名已存在'
        return JsonResponse(response)
    else:
        file = request.POST.get('file')
        print(file)
        file = request.FILES.get('file')
        print(file)

    

# 登录
def login(request):

    if request.method == 'GET':

        return render(request, 'login1.html')

    elif request.method == 'POST1':
        username = request.POST['username']
        password = request.POST['password']
        code = request.POST['code']
        print(request.session['valid_code'])
        print(code.upper())
        if code.upper() != request.session['valid_code'].upper():
            return HttpResponse('验证码错误')
        elif len(password) < 6:
            return HttpResponse('--密码不得小于六位--')
        else:
            m = hashlib.md5()
            m.update(password.encode())
            passwordm = m.hexdigest()
            try:
                use = User.objects.get(name = username, password = passwordm)
            except:
                return HttpResponse('--用户名不存在或密码错误')
            request.session['username'] = username
            request.session['uid'] = use.uid
            resp = HttpResponseRedirect('/home')
            #resp = HttpResponseRedirect('/model')
            if 'remember' in request.POST:
                resp.set_cookie('username', username, 3600 * 24)
                resp.set_cookie('uid', use.uid, 3600 * 24)
            else:
                resp.set_cookie('username', username, 3600)
                resp.set_cookie('uid', use.uid, 3600)
            return resp
    elif request.is_ajax():
        response = {'code':100,'msg':None}
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        print(code.upper())
        print(request.session['valid_code'].upper())
        if request.session['valid_code'].upper()==code.upper():
            m = hashlib.md5()
            m.update(password.encode())
            passwordm = m.hexdigest()
            try: 
                use = User.objects.get(name = username, password = passwordm)
                request.session['username'] = username
                request.session['uid'] = use.uid
                response['uid'] = use.uid
                response['msg'] = '登录成功'
            except:
                response['code']=101
                response['msg'] = '用户名或密码错误'
        else:
            response['code'] = 102
            response['msg'] = '验证码错误'
        return JsonResponse(response)

# 退出登录
def logout(request):
    # 删除session
    del request.session['username']
    del request.session['uid']
    # 删除cookies
    resp = HttpResponseRedirect('/home')
    #resp = HttpResponseRedirect('/model')
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    return resp


#个人信息
@check_login
def msg(request):
    uid = request.COOKIES.get('uid')
    if request.method == 'POST':
        ...
    msg = User.objects.get(uid = int(uid))
    cursor = connection.cursor()
    pub_plate = Plate.objects.raw('select * from plate_plate where plate_root_user_id={}'.format(uid))
    pub_article = Article.objects.raw('select * from msg_article where user_id = {}'.format(uid))
    pub_comment = Comment.objects.raw('select * from msg_comment where user_id = {}'.format(uid))
    #save_user = Follow.objects.get(fan_id=uid)
    save_plate = []
    save_article = Article.objects.raw('select * from msg_article_save_user where user_id = {}'.format(uid))
    save_plate = msg.save_plate.all()
    save_article = msg.save_article.all()
    #save_user = save_user.
    fan = msg.fan_user.all()
    is_follow = 2
    status = 'false'
    if msg.sex == 1:
        sex1 = 'checked'
    else:
        sex2 = 'checked'
    tag = request.GET.get('tag','')
    if tag == '1':
        status1 = 'active'
    elif tag == '2':
        status2 = 'active'
    elif tag == '3':
        status3 = 'active'    
    print(tag)
    return render(request, 'msg2.html', locals())

    
@check_login
def msg_other(request):
    id = int(request.GET['id'])
    msg = User.objects.get(uid = id)
    user = User.objects.get(uid = request.session.get('uid'))
    fan = msg.fan_user.all()
    is_follow = True if Follow.objects.filter(follow = msg, fan = user) else False

    if request.method == 'GET':
        if msg.uid == user.uid:
            is_follow = 2
        status = "readonly = 'true'"
        return render(request, 'msg1.html', locals())
    elif request.method == 'POST':
        if is_follow:
            Follow.objects.get(follow = msg, fan = user).delete()
        else:
            Follow.objects.create(follow = msg, fan = user)
        is_follow = not is_follow 
        return render(request, 'msg1.html', locals())
    

def get_random_color():
    return (randint(0,255), randint(0,255), randint(0,255))

def get_code(request):
    # 自动生成图片
    valid_code = ''
    color = get_random_color()
    img = Image.new('RGB', (350, 40), color)
    # 写文字
    # 生成一个字体对象
    font = ImageFont.truetype('static/font/segoepr.ttf', 34)
    draw = ImageDraw.Draw(img)
    for i in range(5):
        num = str(randint(0, 9))
        up_chr = str(chr(randint(65,90)))
        lower_chr = str(chr(randint(97,122)))
        string = random.choice([num, up_chr, lower_chr])
        valid_code += string
        draw.text((50*i+50, -8), string, font=font, fill=get_random_color())
    request.session['valid_code']=valid_code
    f = BytesIO()
    img.save(f, 'png')
    return HttpResponse( f.getvalue())
    
def update_user(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        print(user_id)
        username = request.POST['username']
        print(username)
        birthday = request.POST['birthday']
        print(birthday)
        sex = request.POST['sex']
        print(sex)
        phone = request.POST['phone']
        print(phone)
        msg = []
        if username:
            msg.append('name="%s"'%username)
        if birthday:
            birthday = birthday.replace('年','-')
            birthday =  birthday.replace('月','-')
            birthday = birthday.replace('日', '-')
            print(birthday)
            msg.append('birthday="%s"'% birthday)
        if sex:
            msg.append('sex=%d'%int(sex))
        if phone:
            msg.append('phone="%s"'%phone)
        if msg:
            msg = ','.join(msg)
            print(msg)
            cursor = connection.cursor()
            print(type(cursor))
            cursor.execute('update user_user set {} where uid = {}'.format(msg, user_id))
            raw = cursor.fetchall()
            #cursor.commit()
            
        return HttpResponseRedirect('/user/msg?tag=3')