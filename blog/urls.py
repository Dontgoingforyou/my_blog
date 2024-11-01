from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import BlogConfig
from .views import ArticleViewSet, CommentViewSet, CategoryViewSet, TagViewSet, article_list
from rest_framework.authtoken.views import obtain_auth_token

app_name = BlogConfig.name

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    # path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    path('', article_list, name='article_list')
]
