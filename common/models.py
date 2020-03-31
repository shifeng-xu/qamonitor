from django.db import models
import django.utils.timezone as timezone
import pytz
from django.db.models import DateTimeField
import mysite
tz = pytz.timezone(mysite.settings.TIME_ZONE)

from mysite import settings

# Create your models here.


class WarnLog(models.Model):
    create_date = models.DateTimeField('记录日期', default=timezone.now)
    real_date = models.DateTimeField('发生日期', auto_now=True)
    content = models.CharField(max_length=1000)
    level = models.CharField(max_length=30)
    #age = models.IntegerField()

class User(models.Model):
    username=models.CharField(max_length=100)
    password = models.CharField(max_length=100)





class JiraRole(models.Model):
    jRoleId = models.CharField(primary_key=True, max_length=100)
    updatetime = DateTimeField(auto_now=True)
    jProject = models.CharField(max_length=100)
    jRole = models.CharField(max_length=100)
    jUrl = models.CharField(max_length=512)

    # unique_together = ("jProject", "restaurant")

class JiraUser(models.Model):
    juid = models.CharField(primary_key=True, max_length=100)
    updatetime = DateTimeField(auto_now=True)
    displayName = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    avatarUrl = models.CharField(max_length=512)
    jRoleId=models.ManyToManyField('JiraRole')

#模块：用于线上问题-产品列表
class Component(models.Model):
    name = models.CharField(max_length=100)
    project = models.CharField(max_length=100)



# jira角色-用户，n:n
#class JiraRole_User(models.Model):
    #jRoleId = models.CharField(max_length=100)
    #juid = models.CharField(max_length=100)
    #updatetime = DateTimeField(auto_now=True)
    #unique_together = ("jRoleId", "juid")