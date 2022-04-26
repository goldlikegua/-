from django.http import HttpResponse
from django.shortcuts import render
from plate.models import Plate
from msg.models import Article
from user.models import User


# Create your views here.
def home_index(request):
    
    plates = []
    plate = Plate.objects.all()
    for i in plate:
        plates.append(i)
    resp = render(request, 'home_index.html', locals())
    if request.session.get('uid') and 'uid' not in request.COOKIES:
        uid = request.session.get('uid')
        resp.set_cookie('uid', uid, 3600 * 24)
    if request.session.get('username') and 'username' not in request.COOKIES:
        username = request.session.get('username')
        resp.set_cookie('username', username, 3600 * 24)
    return resp

def home(request):
    plate = Plate.objects.all()
    plate = list(plate)
    plates = []
    while plate:
        s = []
        s.append(plate.pop(0))
        if plate:
            s.append(plate.pop(0))
        if plate:
            s.append(plate.pop(0))
        plates.append(s)
    resp = render(request, 'home_index1.html', locals())
    if request.session.get('uid') and 'uid' not in request.COOKIES:
        uid = request.session.get('uid')
        resp.set_cookie('uid', uid, 3600 * 24)
        username = request.session.get('username')
        resp.set_cookie('username', username, 3600 * 24)
        print('uid')
    print(request.COOKIES.get('uid'))
    print(plates)
    return resp

def selected_home(request):
    articles = Article.objects.raw('select * from msg_article order by count_comment desc limit 10')
    plates = Plate.objects.raw('select * from plate_plate order by count_title desc limit 10')
    print(articles[0].title)
    resp = render(request,'home1.html', locals())
    if request.session.get('uid') and 'uid' not in request.COOKIES:
        uid = request.session.get('uid')
        resp.set_cookie('uid', uid, 3600 * 24)
        username = request.session.get('username')
        resp.set_cookie('username', username, 3600 * 24)
        print('uid')
    print(request.session.get('uid'))
    print('uid' in request.COOKIES)
    print(plates)
    return resp
    return HttpResponse(resp)

def search(request):
    text = request.GET.get('text')
    plates = Plate.objects.raw('select * from plate_plate where name like "%%{}%%"'.format(text))
    articles = Article.objects.raw('select * from msg_article where title like "%%{}%%"'.format(text))
    users = User.objects.raw('select * from user_user where name like "%%{}%%"'.format(text))
    mg_plate = len(plates)
    mg_article = len(articles)
    mg_user = len(users)
    # article = []
    # for i in range(len(articles)):
    #     if i%4 == 0:
    #         article.append([])
    #     article[-1].append(articles[i])
    # plate = []
    # for i in range(len(plates)):
    #     if i%3 == 0:
    #         plate.append([])
    #     plate[-1].append(plates[i])
    # plates = plate
    print(mg_plate)
    print(mg_article)
    return render(request, 'search.html', locals())