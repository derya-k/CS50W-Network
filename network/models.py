from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', blank=True, related_name='u_followers', symmetrical=False)
    following = models.ManyToManyField('self', blank=True, related_name='u_following', symmetrical=False)

    def serialize(self):
        return{
            "id":self.id,
            "username":self.username,
            "followers":self.followers.all().count(),
            "following": self.following.all().count(),

        }

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="author")
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,blank=True, related_name="likes")

    def serialize(self):
        return{
            "id":self.id,
            "author":self.author,
            "body":self.body,
            "date":self.date.strftime("%b %d %Y, %I:%M %p"),
            "likes":self.likes.count()
        }
