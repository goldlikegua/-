from email.policy import default
from django.db import models
from django.db import models
from django.db.models.deletion import CASCADE,PROTECT
from django.db.models.fields import related
from plate.models import Plate
from user.models import User

# Create your models here.
class Article(models.Model): # 主题
    tid = models.AutoField(primary_key=True)
    title = models.CharField('标题', max_length=50)
    content = models.TextField('内容', blank=True)
    is_active = models.BooleanField('是否活跃', default=True)
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    plate = models.ForeignKey(to=Plate, related_name='article', on_delete=CASCADE)
    user = models.ForeignKey(to=User, related_name='create_article', on_delete=CASCADE)
    save_user = models.ManyToManyField(User, related_name='save_article')
    count_comment = models.IntegerField('热度', default=0)
    is_good = models.BooleanField('精选', default=False)

class Comment(models.Model):  # 评论
    pid = models.AutoField(primary_key=True)
    content = models.TextField('内容')
    add_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField('状态',default=0)
    article = models.ForeignKey(to=Article, related_name='comment', on_delete=PROTECT)
    user = models.ForeignKey(to=User, related_name='comment', on_delete=CASCADE)
