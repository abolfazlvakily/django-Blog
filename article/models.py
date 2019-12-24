from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.translation import ugettext as _
import uuid


class Person(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    phone_number = models.CharField(max_length=150)
    address = models.CharField(max_length=300)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        db_table = 'persons'


class Article(models.Model):
    person_id = models.ForeignKey('Person', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name=_('post_title'))
    content = RichTextField()
    hash_id = models.SlugField(unique=True, default=uuid.uuid1)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('post_created_date'))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        db_table = 'articles'


class Attachment(models.Model):
    post_id = models.ForeignKey('Article', on_delete=models.CASCADE)
    file = models.FileField(blank=True, null=True, verbose_name=_('post_file'))

    class Meta:
        db_table = 'attachment'


class Comment(models.Model):
    post_id = models.ForeignKey('Article', on_delete=models.CASCADE, related_name="comments")
    comment_author = models.CharField(max_length=50, verbose_name=_('comment_author'))
    comment_content = models.CharField(max_length=200, verbose_name=_('comment_content'))
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ['-comment_date']
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        db_table = 'comments'
