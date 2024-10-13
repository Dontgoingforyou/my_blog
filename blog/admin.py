from django.contrib import admin

from blog.models import Category, Tag, Article, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'content', 'created_at', 'updated_at',)
    list_filter = ('author', 'title', 'created_at')
    search_fields = ('author', 'categories', 'title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'context', 'created_at')
    list_filter = ('author', 'article', 'created_at')
    search_fields = ('author', 'title')