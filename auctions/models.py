from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Categories(models.Model):
    category = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.category


class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=10000)
    picture = models.URLField()
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_DEFAULT,
        related_name="categories",
        default=1
    )
    status = models.BooleanField(default=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    watchlist = models.ManyToManyField(User, blank=True, related_name="l_watchlist")

    def __str__(self):
        return f"{self.title}"


class Comments(models.Model):
    comment = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_user")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments_listing")

    def __str__(self):
        return f"{self.comment}\nfrom user: {self.user}"


class Bids(models.Model):
    cost = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_user")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids_listing")

    def __str__(self):
        return f'cost: {self.cost}\nusers: {self.user}\nlistings: {self.listing}'
