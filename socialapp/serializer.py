from rest_framework import serializers
from django.contrib.auth.models import User
from socialapp.models import UserProfile,Posts,Comments


class UserSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    class Meta:
        model=User
        fields=[
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "password"

        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class UserProfileSerializer(serializers.ModelSerializer):

    user=serializers.CharField(read_only=True)

    class Meta:
        model=UserProfile
        fields="__all__"





class CommentsSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    post=serializers.CharField(read_only=True)
    class Meta:
        model=Comments
        fields="__all__"

    def create(self, validated_data):
        user=self.context.get("user")
        post=self.context.get("post")
        return Comments.objects.create(**validated_data,user=user,post=post)

class PostsSerializer(serializers.ModelSerializer):
    author=serializers.CharField(read_only=True)
    get_comments=CommentsSerializer(many=True,read_only=True)
    get_like=serializers.CharField(read_only=True)
    like=UserSerializer(read_only=True,many=True)
    get_like_count=serializers.CharField(read_only=True)
    class Meta:
        model=Posts
        fields="__all__"






