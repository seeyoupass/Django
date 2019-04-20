from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Catelory(models.Model):
    """
        Django 要求模型必须继承 models.Model 类。
        Category 只需要一个简单的分类名 name 就可以了。
        CharField 指定了分类名 name 的数据类型，CharField 是字符型，
        CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
        当然 Django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
        Django 内置的全部类型可查看文档：
        https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
        """
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Post(models.Model):
    title=models.CharField(max_length=100)
    body=models.TextField()
    create_time=models.DateTimeField()
    #最后一次修改时间
    modified_time=models.TimeField()
    #文章摘要，black=True，允许值为空
    excerpt=models.CharField(max_length=255,blank=True)
    #ForeignKey代表一对多的关联关系，即一个分类可以对于多篇文章，而文章只能对应一个分类
    catelory=models.ForeignKey(Catelory,on_delete=models.CASCADE)
    #ManyToManyField代表多对多的关联关系
    tag=models.ManyToManyField(Tag)
    #User表示从django.contrib.auth.models 导入的
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('mysite:detail',kwargs={'pk':self.pk})
