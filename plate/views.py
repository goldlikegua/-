from django.http import JsonResponse, response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from plate.models import Plate
from user.models import User
from msg.views import check_login,detect
from django.db import connection

# Create your views here.
@check_login
def index(request, id):
    uid = request.COOKIES.get('uid')
    root_user = 0
    is_save = 0
    plate = Plate.objects.get(id = id)
    if uid and plate.plate_root_user.uid == int(uid):
        root_user = 1
    if uid and Plate.objects.raw('select * from plate_plate_save_user where plate_id={} and user_id={}'.format(id, uid)):
        is_save = 1
    order = request.GET.get('order')
    order = order if order else '-update_time'
    if order == 'is_good':
        articles = plate.article.filter(is_good = True)
    else:
        articles = plate.article.all().order_by(order)
    plate.count_title = len(articles)
    plate.save()
    return render(request, 'plate_articles1.html', locals())
    return render(request, 'plate_index.html', locals())

@check_login
def add_plate(request):

    if request.method == 'GET':
        return render(request, 'add_plate1.html')

    elif request.is_ajax():
        response = {'code':100,'title':None}
        try:
            uid = request.COOKIES.get('uid')
            user = User.objects.get(uid = uid)
        except:
            return HttpResponseRedirect('/user/login')
        name = request.POST.get('name')
        msg = request.POST.get('msg')
        if detect(name) or detect(msg):
            response['code'] = 102
            response['title'] = '系统检测到您的言论中有不良词汇，请自检后再发表，让我们共同维护论坛的和谐良好风气'
        elif Plate.objects.filter(name = name):
            response['code'] = 101
            response['title'] = '板块名已存在'
        else:
            Plate.objects.create(name = name, msg = msg, plate_root_user = user)
            response['code'] = 100
            response['title'] = '创建成功'
        #print(3333)
        return JsonResponse(response)
    
    elif request.method == 'POST':
        try:
            uid = request.COOKIES.get('uid')
            user = User.objects.get(uid = uid)
        except:
            return HttpResponseRedirect('/user/login')
        name = request.POST['name']
        msg = request.POST['msg']
        if Plate.objects.filter(name = name):
            return HttpResponse('板块名已存在')
        Plate.objects.create(name = name, msg = msg, plate_root_user = user)
        return HttpResponse('创建成功')
    
    


def plate_msg(request):
    if request.method == 'GET':
        id = request.GET['id']
        plate = Plate.objects.get(id=id)
        return render(request, 'plate_msg.html', locals())

@check_login
def delete_plate(request):
    if request.method == 'POST':
        uid = request.COOKIES.get('uid')
        plate_id = request.POST['plate_id']
        print(uid)
        print(plate_id)
        print(type(uid))
        print(type(plate_id))
        Plate.objects.get(plate_root_user=uid,id=plate_id).delete()
        return HttpResponseRedirect('/')

@check_login
def save_plate(request):
    if request.method == 'POST':
        plate_id = request.POST['id']
        user_id = request.COOKIES.get('uid')
        print(plate_id)
        print(user_id)
        cursor = connection.cursor()
        plate = Plate.objects.raw('select * from plate_plate_save_user where plate_id = {} and user_id = {}'.format(plate_id, user_id))
        if plate:
            cursor.execute('delete from plate_plate_save_user where plate_id = {} and user_id = {}'.format(plate_id, user_id))
            raw = cursor.fetchall() 
        else:          
            cursor.execute('insert into plate_plate_save_user set plate_id = {},user_id = {}'.format(plate_id, user_id))
            raw = cursor.fetchall() 
        return HttpResponseRedirect('/plate/index/{}'.format(plate_id))