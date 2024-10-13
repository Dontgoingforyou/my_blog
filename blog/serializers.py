from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article, Comment, Category, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'article', 'author', 'content', 'created_at']


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Article
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'categories', 'tags', 'comments']

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        tags_data = validated_data.pop('tags', [])
        article = Article.objects.create(**validated_data)
        for category in categories_data:
            category_obj, created = Category.objects.get_or_create(name=category['name'])
            article.categories.add(category_obj)
        for tag in tags_data:
            tag_obj, created = Tag.objects.get_or_create(name=tag['name'])
            article.tags.add(tag_obj)
        return article

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories', [])
        tags_data = validated_data.pop('tags', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if categories_data:
            instance.categories.clear()
            for category in categories_data:
                category_obj, created = Category.objects.get_or_create(name=category['name'])
                instance.categories.add(category_obj)

        if tags_data:
            instance.tags.clear()
            for tag in tags_data:
                tag_obj, created = Tag.objects.get_or_create(name=tag['name'])
                instance.tags.add(tag_obj)
            return instance
