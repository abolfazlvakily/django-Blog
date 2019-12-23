from django.urls import path
from .views import Article, Login, Logout

app_name = 'article'
urlpatterns = [
    path('', Article.as_view(), name='article'),
    path('<uuid:hash_id>/', Article.as_view(), name='detail'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
