from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from precise_bbcode import fields

def user_media_path(instance, filename):
    return 'user_{}/{}'.format(instance.author.id, filename)
    
def user_profile_media_path(instance, filename):
    return 'user_{}/{}'.format(instance.user.id, filename)

# Create your models here.
class Post(models.Model):
    STATUS_CHOICES= (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = fields.BBCodeTextField(verbose_name='Описание')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    rubric = models.ForeignKey('Rubric', on_delete=models.PROTECT, null=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    fixed = models.BooleanField(default=False)
    image = models.CharField(max_length=250, blank=True, null=True)
    likes = GenericRelation('Like')    

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

class Rubric(models.Model):

    name = models.CharField(max_length=250)
    image = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name = "Рубрика"
        verbose_name_plural = "Рубрики"
        ordering = ('name',)

    def __str__(self):
        return self.name

class TodaySchedule(models.Model):

    lesson_numb = models.SmallIntegerField(primary_key=True, default=0)
    subject = models.CharField(max_length=10, verbose_name='Предмет')
    lessonType = models.CharField(max_length=10)
    startLessonTime = models.TimeField()
    endLessonTime = models.TimeField()
    auditory = models.CharField(max_length=10)
    employee = models.CharField(max_length=40, verbose_name='Преподаватель')
    note = models.CharField(max_length=70, blank=True, null=True, default='')

    class Meta:
        verbose_name = 'Пара'
        verbose_name_plural = 'Пары'

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.CharField(max_length=200, default='no-avatar-300x300.jpg')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    publish = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    profile = models.ForeignKey(UserProfile, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-publish']
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        if len(self.body) > 50:
            return self.body
        return self.body[:50]+"..."

class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
