from statistics import mode
from django.db import models

# Create your models here.



class Books(models.Model):
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=30, blank=True, null=True)

    # django web
    class Meta:
        verbose_name='book'
        verbose_name_plural=verbose_name    # 复数形式
        db_table = 'books'        # 数据库表的名字
    def __str__(self):
        return self.name