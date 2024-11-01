from django.shortcuts import render
from rest_framework import viewsets
from .models import Article, Category, Comment, Tag
from .serializers import ArticleSerializer, CategorySerializer, CommentSerializer, TagSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    """ CRUD для статей """

    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Article.objects.all().order_by('-created_at')
        category = self.request.query_params.get('category')
        tag = self.request.query_params.get('tag')
        search = self.request.query_params.get('search')

        if category:
            queryset = queryset.filter(categories__name__icontains=category)
        if tag:
            queryset = queryset.filter(tags__name__icontains=tag)
        if search:
            queryset = queryset.filter(title__icontains=search) | queryset.filter(content__icontains=search)
        return queryset.distinct()


class CommentViewSet(viewsets.ModelViewSet):
    """ CRUD для комментариев """

    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    """ CRUD для категории """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    """ CRUD для тегов """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'blog/base.html', {'articles': articles})