from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import *
import jieba
from django.db import connection
def check_article(func):
#检查主题是否存在
    def wrap(request, *args, **kwargs):
        try:
            id = request.GET.get('id')
        except:
            return HttpResponse('该文章不存在')
        return func(request, *args, **kwargs)
    return wrap

def check_login(func):
# 检查用户是否登录
    def wrap(request, *args, **kwargs):
        print(request.session.values())
        
        if not request.session.get('username') or not request.session.get('uid'):
            if 'uid' not in request.COOKIES or 'username' not in request.COOKIES:
                return HttpResponseRedirect('/user/login')
        return func(request, *args, **kwargs)
    return wrap

def detect(txt):
# 检测言论中是否包含敏感词
    f = open('static/detect.txt','r',encoding='utf-8')
    lis = []
    for i in f.readlines():
        if i:
            lis.append(i[:-1])
    f.close()
    for i in jieba.lcut(txt):
        if i in lis:
            print(i)
            return True
    print(lis[0])
    return False


@check_article
@check_login
def article(request):
    id = request.GET.get('id')
    uid = request.COOKIES.get('uid')
    error = request.GET.get('error','')
    article = Article.objects.get(tid=id)
    if uid and article.user.uid == int(uid):
        is_root = 1
    else:
        is_root = 0
    plate = article.plate
    user = article.user
    comment = article.comment.all()
    count = len(comment)
    is_save=0
    cursor = connection.cursor()
    cursor.execute('select id from msg_article_save_user where article_id={} and user_id={}'.format(id, uid))
    raw = cursor.fetchall() 
    if uid and raw:
        is_save = 1
    print(is_save)
    print(count)
    return render(request, 'article_index1.html', locals())

@check_login
def add_article(request):
    plate_id = request.GET.get('plate_id')
    print(plate_id)
    print(type(plate_id))
    if request.method == 'GET':
        return render(request, 'add_article1.html', locals())
    elif request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        if not title:
            return HttpResponseRedirect('/plate/index/%s' % plate_id)
        elif detect(title) or detect(content):
            return HttpResponse('敏感词')
        user_id = request.session.get('uid')
        plate = Plate.objects.get(id = plate_id)
        user = User.objects.get(uid = user_id)
        try:
            Article.objects.create(title=title, content=content, plate=plate, user=user)
        except:
            return HttpResponse('发表失败')
        return HttpResponseRedirect('/plate/index/%s' % plate_id)


@check_article
@check_login
def add_comment(request):
    id = request.POST['id']
    uid = request.COOKIES['uid']
    comment = request.POST['comment']
    is_detect = 0
    if not comment:
        print(1)
        return HttpResponseRedirect('/msg/article?id=%s' % id)
    if detect(comment):
        error = '系统检测到您的言论中有不良词汇，请自检后再发表，让我们共同维护论坛的和谐良好风气'
        is_detect = 1
        print(is_detect)
        return HttpResponseRedirect('/msg/article?id=%s' % (id), locals())
    user = User.objects.get(uid = uid)
    article = Article.objects.get(tid = id)
    coms = Comment.objects.create(content=comment, user=user, article=article)
    article.update_time = coms.add_time
    article.count_comment = len(article.comment.all())
    article.save()
    return HttpResponseRedirect('/msg/article?id=%s' % id)

@check_article
@check_login
def selected_article(request):
    if request.method == 'POST':
        tid = request.POST['tid']
        plate_id = request.POST['plate_id']
        user_id = request.COOKIES.get('uid')
        plate = Plate.objects.raw('select * from plate_plate where id={} and plate_root_user_id={} limit 1'.format(plate_id, user_id))
        if plate:
            article = Article.objects.get(tid=tid)
            print(article)
            if article:
                is_good = 0 if article.is_good else 1
                article.is_good = is_good
                article.save()
        return HttpResponseRedirect('/plate/index/{}'.format(plate[0].id))
    
@check_login
def delete_article(request):
    if request.method == 'POST':
        tid = request.POST['tid']
        user_id = request.COOKIES.get('uid')
        article = Article.objects.raw('select * from msg_article where tid={}'.format(tid))
        plate_id = article[0].plate_id
        plate = Plate.objects.raw('select * from plate_plate where id={}'.format(plate_id))
        if str(plate[0].plate_root_user_id) == user_id or str(article[0].user_id) == user_id:
            a = Article.objects.get(tid=tid)
            Comment.objects.filter(article = a).delete()
            Article.objects.get(tid=tid).delete()
        if user_id == str(plate[0].plate_root_user_id):
            resp = '/plate/index/{}'.format(plate[0].id)
        else:
            resp = '/user/msg_other?id={}'.format(user_id)
        return HttpResponseRedirect(resp)

@check_login
def delete_comment(request):
    if request.method == 'POST':
        pid = request.POST['pid']
        print(pid)
        user_id = request.COOKIES.get('uid')
        comment = Comment.objects.raw('select * from msg_comment where pid={}'.format(pid))
        article = Article.objects.raw('select * from msg_article where tid={}'.format(comment[0].article_id))
        print(comment[0].user_id)
        print(article[0].user_id)
        print(user_id)
        if user_id == str(comment[0].user_id) or user_id == str(article[0].user_id):
            comment = Comment.objects.get(pid=pid).delete()
            print(comment)
            return HttpResponseRedirect('/msg/article?id={}'.format(article[0].tid))
        else:
            return HttpResponse('123')


@check_login
def save_article(request):
    if request.method == 'POST':
        article_id = request.POST['id']
        user_id = request.COOKIES.get('uid')
        print(user_id)
        cursor = connection.cursor()
        cursor.execute('select * from msg_article_save_user where article_id = {} and user_id = {}'.format(article_id, user_id))
        raw = cursor.fetchall() 
        if raw:
            cursor.execute('delete from msg_article_save_user where article_id = {} and user_id = {}'.format(article_id, user_id))
            raw = cursor.fetchall() 
            print(11)
        else:          
            cursor.execute('insert into msg_article_save_user set article_id = {},user_id = {}'.format(article_id, user_id))
            raw = cursor.fetchall()
            print(22) 
        return HttpResponseRedirect('/msg/article?id={}'.format(article_id))