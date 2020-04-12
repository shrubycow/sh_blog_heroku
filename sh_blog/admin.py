from django.contrib import admin
from .models import Post, Rubric, UserProfile, Comment
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'rubric','slug', 'author', 'publish', 'status', 'fixed')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')
    search_fields = ('user',)
    ordering = ('user',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'body', 'publish')
    search_fields = ('post', 'body')
    ordering = ('publish',)