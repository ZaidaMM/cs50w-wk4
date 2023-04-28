from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category_name}"
    
class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="userBid")

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=400)
    starting_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, related_name="startingBid", default=0)
    image_url = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="category")
    is_active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlistListing")
    bid_counter = models.IntegerField(default = 1)

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="userComment")
    text = models.TextField(blank=True, max_length=300)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, related_name="listingComment")

    def __str__(self):
        return f"{self.author}: {self.text}"