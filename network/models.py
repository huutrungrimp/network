from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify

class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    bio = models.TextField(max_length=500, null=True)
    myfollowers = models.IntegerField(default=0)
    myleaders = models.IntegerField(default=0)

    def __str__(self):
        return self.username
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            'bio': self.bio,
        }


class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, unique=True)
    content = models.TextField()
    date_created = models.DateTimeField(null=False, auto_now_add=True)

    def __str__(self):
        return str(self.title)


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username.username,
            "title": self.title,
            "content": self.content,
            "date_created": self.date_created.strftime("%m/%d/%Y, %H:%M:%S"),
        }


class Liking(models.Model):    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    bywhom = models.ForeignKey(User, on_delete=models.CASCADE)
    
    LIKING_STATUS = (
        ('Like', 'Like'),
        ('Unlike', 'Unlike'),
    )

    preference = models.CharField(
        max_length = 7,
        choices = LIKING_STATUS,
        default = 'Like',
        null = True,
    )


    def __str__(self):
        return str(self.bywhom)


class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.username)



class Friendship(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fr_user')
    followers = models.ForeignKey(User, related_name='fr_followers', on_delete=models.CASCADE, null=True, blank=True)
    leaders = models.ForeignKey(User, related_name='fr_leaders', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.username) + ' ,  ' + str(self.followers)

    def serialize(self):
        return {
            'username': self.username,
            'followers': self.followers.username,
            'leaders': self.leaders.username,
        }