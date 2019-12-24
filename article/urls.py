from django.urls import path
from .views import Article, Comment

app_name = 'article'
urlpatterns = [
    path('', Article.as_view(), name='article'),
    path('<uuid:hash_id>/', Article.as_view(), name='detail'),
    path('<uuid:hash_id>/add_comment/', Comment.as_view(), name='add_comment'),
]
