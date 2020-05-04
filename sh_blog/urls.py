from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, post_detail, not_about_work, by_rubric, test, add_or_remove_like

app_name = 'sh_blog'

urlpatterns = [
    path('', index, name='main'),
    path('rubrics/', not_about_work, name='not_work'),
    path('rubrics/<int:pk>/', by_rubric, name='by_rubric'),
    path('test/', test, name="test"),
    path('like/<int:post_or_comment>/<int:object_id>/', add_or_remove_like, name="like" ),
    path('<slug:slug>/', post_detail, name='detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)