from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=48)

    def __str__(self):
        return f"{self.category_name}"



class Listing(models.Model):
    title = models.CharField(max_length=24)
    startPrice = models.FloatField()
    details = models.TextField(max_length=300)
    image = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    created = models.DateField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Listing ID: {self.id}, Title: {self.title}, Price :{self.startPrice}"

class Bid(models.Model):
    bid_amt = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="topbidder")
    bid_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, related_name="listingbids")

    def __str__(self):
        return f"Bid ID: {self.id}, Listing ID: {self.bid_listing.title}, Amount: {self.bid_amt}, User: {self.bidder}"


class Comment(models.Model):
    commenter = models.TextField()
    comment = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    date = models.DateField()

    def __str__(self):
        return f"Comment ID: {self.id}, Commenter: {self.commenter}, Comment: {self.comment}, Listing: {self.listing}"

class Watchlist(models.Model):
    watchUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")
    watchedListing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingwatch")

    def __str__(self):
        return f"Watched Listing ID: {self.id}, Listing: {self.watchedListing}, User: {self.watchUser}"