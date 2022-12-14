from django.shortcuts import render
from django.contrib.auth.models import User
from socialapp.models import UserProfile,Posts,Comments
from socialapp.serializer import UserSerializer,UserProfileSerializer,PostsSerializer,CommentsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.

class UserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()





class UserProfileView(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

    @action(methods=["post"],detail=True)
    def follow(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        user=User.objects.get(id=id)
        profile=UserProfile.objects.get(user=request.user)
        profile.followers.add(user)
        return Response({"msg":"You are following "+str(user.first_name)})

    @action(methods=["get"],detail=False)
    def get_followings(self,request,*args,**kwargs):
        user=request.user
        followings=user.followers.all()
        serializer=UserProfileSerializer(followings,many=True)
        return Response(data=serializer.data)

    @action(methods=["get"],detail=False)
    def get_suggestions(self,request,*args,**kwargs):
        suggetions=User.objects.exclude(id=request.user.id)
        serializer=UserSerializer(suggetions,many=True)
        return Response(data=serializer.data)






    # def create(self,request,*args,**kwargs):
    #     user=request.user
    #     serializer=UserProfileSerializer(data=request.data,context={"user":user})
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)


class Postsview(ModelViewSet):
    serializer_class = PostsSerializer
    queryset = Posts.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=["post"],detail=True)
    def add_comment(self,request,*args,**kwargs):
        post_id=kwargs.get("pk")
        post=Posts.objects.get(id=post_id)
        user=request.user
        serializer=CommentsSerializer(data=request.data,context={"user":user,"post":post})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.validated_data)
        else:
            return Response(data=serializer.errors)

    @action(methods=["get"],detail=True)
    def fetch_comments(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        comment=post.comments_set.all()
        serializer=CommentsSerializer(comment,many=True)
        return Response(data=serializer.data)

    @action(methods=["post"],detail=True)
    def add_like(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        post.like.add(request.user)
        return Response("Like Added")


    # @action(methods=["update"],detail=True)
    # def add_like(self,request,*args,**kwargs):
    #     post=Posts.






