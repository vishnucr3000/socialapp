from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_image=models.ImageField(upload_to="profile_images",null=True)
    dob=models.DateField()
    address=models.CharField(max_length=250)
    mobile=models.CharField(max_length=10)
    options=(
        ("Male","Male"),
        ("Female","Female")
    )
    gender=models.CharField(max_length=6,choices=options,default="male")

class Posts(models.Model):
    title=models.CharField(max_length=50)
    post_image=models.ImageField(upload_to="post_images",null=True)
    description=models.CharField(max_length=250)
    post_date=models.DateField(auto_now_add=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="post")
    like=models.ManyToManyField(User)

    def get_comments(self):
        return self.comments_set.all()
    def get_like_count(self):
        return self.like.all().count()

class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment=models.CharField(max_length=250)
    comment_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment


