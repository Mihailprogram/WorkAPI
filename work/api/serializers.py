from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from .models import Component, Parametrs, Category
from django.shortcuts import get_object_or_404

User = get_user_model()


class CreatUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password')


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',)
        

class TokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})


class ComponentSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='namecategory')
    parametrs = serializers.SerializerMethodField()

    class Meta:
        model = Component
        fields = ('id', 'title_categories', 'category', 'parametrs')
    
    def get_parametrs(self, obj):
        slov = {}
        parametr = obj.parametrs
        slov['сontent'] = parametr.сontent
        slov['humidity'] = parametr.humidity
        slov['contentmass'] = parametr.contentmass
        slov['heatmass'] = parametr.heatmass

        return slov

    def create(self, validated_data):
        user = User.objects.get(email=self.context['request'].user)
        context = self.context['request'].data

        category, _ = Category.objects.get_or_create(namecategory=context['category'])
        parametrs = Parametrs.objects.create(**context['parametrs'])
        component = Component.objects.create(category=category,
                                             parametrs=parametrs, 
                                             title_categories=context['title_categories'],
                                             user=user)

        return component