from django import template
from django.contrib.contenttypes.models import ContentType
from sh_blog.models import Like

register = template.Library()

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter
def is_fan(obj, user) -> bool:
    """Проверяет, лайкнул ли 'user' объект 'obj'"""
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    return Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user).exists()