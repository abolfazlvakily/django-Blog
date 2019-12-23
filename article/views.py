from django.shortcuts import render, HttpResponse
from . import models
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout
from django.views.generic import View
from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _


class Login(View):
    @staticmethod
    def get(request):
        return render(request, 'auth/login.html')

    @staticmethod
    def post(request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('article:article'))
        else:
            context = {
                'error': _('username or password is not valid')
            }
            return render(request, 'auth/login.html', context)


class Logout(View):
    @staticmethod
    def get(request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('article:article'))


class Article(AccessMixin, View):
    login_url = reverse_lazy('admin:login')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.hash_id = kwargs.pop('hash_id', None)
        return super(Article, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        # detail
        if self.hash_id is not None:
            article = get_object_or_404(models.Article, hash_id=self.hash_id)
            context = {
                'post': article
            }
            return render(request, 'article/article_detail.html', context)
        else:
            # list
            return HttpResponse('list of articles ...')

    def post(self, request):
        # add
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        else:
            return HttpResponse('posts will add ....')

    def delete(self, request):
        # delete
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif self.hash_id is not None:
            models.Article.objects.filter(hash_id=self.hash_id)
            return HttpResponse('ok deleted!!!')

    def update(self, request):
        # update
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif self.hash_id is not None:
            return HttpResponse('will update ...')


class Comment(View):
    def dispatch(self, request, *args, **kwargs):
        self.hash_id = kwargs.pop('hash_id', None)
        self.article = get_object_or_404(models.Article, hash_id=self.hash_id)
        return super(Comment, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def get(request):
        return render(request, 'article/comment.html')

    def post(self, request):
        comment_author = request.POST['author']
        comment_content = request.POST['content']
        models.Comment.objects.create(
            post_id=self.article.id,
            comment_author=comment_author,
            comment_content=comment_content
        )
        return HttpResponseRedirect(reverse_lazy('article:detail', kwargs={'hash_id': self.hash_id}))
