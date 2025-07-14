from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class Post(models.Model):
     
    text = models.CharField(max_length= 500)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    time=models.DateTimeField(auto_now_add = True)
    likes = models.ManyToManyField(User,blank=True, related_name="likes")    
     
    
    def __str__(self):
        return f"{self.user} posted {self.text} on {self.time.strftime('%d %b %Y %H:%M:%S')}"
    
class Follow(models.Model):
    followerID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follows")
    followedID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_by" )

    def __str__(self):
        return f"{self.followerID} follows {self.followedID}"
    
    
         