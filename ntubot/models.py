from django.db import models

# Create your models here.

class User_Info(models.Model):
    uid = models.CharField(max_length=50,null=False,default='') #user_id
    name = models.CharField(max_length=255,blank=True,null=False) #LINE名字
    section = models.PositiveIntegerField(default=0) #關卡
    part = models.PositiveIntegerField(default=0) #關卡內段落
    hint = models.PositiveIntegerField(default=0) #提示段落
    total_hint = models.PositiveIntegerField(default=0) #總提示

    def __str__(self):
        return self.uid