from django.db import models

# Create your models here.

class User_Info(models.Model):
    uid = models.CharField(max_length=50,null=False,default='')         #user_id
    name = models.CharField(max_length=255,blank=True,null=False)       #LINE名字
    section = models.PositiveIntegerField(default=0)
    part = models.PositiveIntegerField(default=0)
    hint = models.PositiveIntegerField(default=0)
    total_hint = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.uid