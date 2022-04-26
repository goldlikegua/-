from email.policy import default
from django.db import models
from django.db.models.deletion import PROTECT
from django.db.models.fields import related
from user.models import User

# Create your models here.
class Plate(models.Model): # 板块基本信息
    name = models.CharField('板块名称', max_length=15)
    #logo = models.ImageField('板块logo', blank=True)
    msg = models.TextField('简介', default='版主没有留下任何信息')
    is_active = models.BooleanField('是否活跃', default=True)
    count_title = models.IntegerField('主题数', default=0)
    plate_root_user = models.ForeignKey(to = User, related_name='create_plate', on_delete=PROTECT)
    save_user = models.ManyToManyField(User, related_name='save_plate')
    CreateTime = models.DateTimeField('创建时间', auto_now_add=True,blank=True)
    #createtime=models.DateTimeField(auto_now_add=True,null=True,blank=True)