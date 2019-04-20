from ..models import Post,Catelory
from django import template


register=template.Library()
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('create_time')[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('create_time', 'month', order='DESC')

@register.simple_tag
def get_catlories():
    # 别忘了在顶部引入 Category 类
    return Catelory.objects.all()
