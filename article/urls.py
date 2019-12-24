from django.urls import path
from .views import Article

app_name = 'article'
urlpatterns = [
    path('', Article.as_view(), name='article'),
    path('<uuid:hash_id>/', Article.as_view(), name='detail'),
]
