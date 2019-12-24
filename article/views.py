from django.shortcuts import render, HttpResponse
from . import models
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from .forms import CommentForm


class Article2(AccessMixin, View):
    login_url = reverse_lazy('admin:login')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.hash_id = kwargs.pop('hash_id', None)
        return super(Article2, self).dispatch(request, *args, **kwargs)

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

    def post(self, request):
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment_author = form.cleaned_data.get('comment_author')
            comment_content = form.cleaned_data.get('comment_content')
            models.Comment.objects.create(
                post_id=self.article,
                comment_author=comment_author,
                comment_content=comment_content
            )
            return HttpResponseRedirect(reverse_lazy('article:detail', kwargs={'hash_id': self.hash_id}))


class Article(Article2):
    # this article added comment form on detail comment
    def get(self, request):
        # detail
        if self.hash_id is not None:
            comment_form = CommentForm()
            article = get_object_or_404(models.Article, hash_id=self.hash_id)
            context = {
                'post': article,
                'comment_form': comment_form
            }
            return render(request, 'article/article_detail.html', context)
        else:
            # list
            return HttpResponse('list of articles ...')
