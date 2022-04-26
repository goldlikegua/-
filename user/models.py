from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class User(models.Model):  # 个人信息
    uid = models.AutoField('账号', primary_key=True)
    name = models.CharField('用户名', max_length=20)
    password = models.CharField('密码', max_length=32)
    sex_choice = (
        (0, '女'),(1, '男')
    )
    sex = models.IntegerField('性别', choices=sex_choice, default=1)
    birthday = models.DateTimeField('生日', default='1999-1-1')
    add_time = models.DateTimeField(auto_now_add=True)
    phone = models.CharField('手机号', max_length=12, null=True)
    level = models.IntegerField('等级', default=1)
    exp = models.IntegerField('经验值', default=0)


class Follow(models.Model):  # 关注和粉丝
    follow = models.ForeignKey(User,related_name='follow_user', on_delete=CASCADE)
    fan = models.ForeignKey(User, related_name='fan_user',on_delete=CASCADE)

# class Saves(models.Model): # 收藏
    
#     user = models.ForeignKey(User, related_name='saves', on_delete=CASCADE)
#     plates = models.ForeignKey(Plate, on_delete=CASCADE)
#     articles = models.ForeignKey(Article, on_delete=CASCADE)

