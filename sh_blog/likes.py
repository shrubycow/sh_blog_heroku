from django.contrib.contenttypes.models import ContentType
from .models import Like

def add_like(obj, user):
    """Лайкает obj"""
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(content_type=obj_type, object_id=obj.id, user=user)
    return like

def remove_like(obj, user):
    """Убирает лайк в obj"""
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user).delete()

def is_fan(obj, user) -> bool:
    """Проверяет, лайкнул ли 'user' объект 'obj'"""
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    return Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user).exists()