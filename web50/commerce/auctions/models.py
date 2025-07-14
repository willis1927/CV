from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(decimal_places=2,max_digits=10, default=0)

class Listing(models.Model):
    class Categories(models.TextChoices):
        Clothing = 'Clothing', ('Clothing')
        Animals = 'Animals', ('Animals')
        Wands = 'Wands', ('Wands')
        Potions = 'Potions', ('Potions')
        Consumables = 'Consumables', ('Consumables')
        Misc = 'Misc', ('Misc')
     

    listingID = models.AutoField(primary_key=True)
    name = models.CharField(max_length= 64)
    description = models.CharField(max_length=500)
    category = models.CharField(choices=Categories.choices, default='Misc', max_length=50)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bids")
    imageURL = models.URLField(null=True, blank=True)
    active=models.BooleanField(default='True')
    owner=models.ForeignKey(User, on_delete=models.CASCADE)
    watches = models.ManyToManyField(User,blank=True, related_name="watched")
    
    def __str__(self):
        return f"{self.name} posted by {self.owner}, price - {self.price}"




    
    
class Comment(models.Model):

    commentID = models.AutoField(primary_key=True)
    listingID = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingComments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userComments")
    text = models.CharField(max_length = 200)
    time=models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"User - {self.user}, Comment -{self.text}"     
    
