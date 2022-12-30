from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    """用户表"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', unique=True)
    avatar = models.CharField(max_length=100, null=True, blank=True, verbose_name="avatar")
    role = models.CharField(max_length=10, default="tester", verbose_name="role")

    class Meta:
        verbose_name = "UserProfile"
        verbose_name_plural = verbose_name
        # db_table = 'users'

    def __str__(self):
        return "{}".format(self.user.__str__())
