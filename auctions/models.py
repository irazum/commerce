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
    # cost = models.IntegerField()
    picture = models.URLField()
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_DEFAULT,
        related_name="categories",
        default=1
    )
    # смысл в том, что seller должен ссылать на зарегистрированного юзера
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.title}"


class Comments(models.Model):
    comment = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_user")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments_listing")

    def __str__(self):
        return f"{self.comment}\nfrom user: {self.user}"


class Bids(models.Model):
    cost = models.IntegerField(unique=True)
    users = models.ManyToManyField(User, related_name="bids_users")
    listings = models.ManyToManyField(Listings, related_name="bids_listings")

    def __str__(self):
        return f'cost: {self.cost}\nusers: {self.users}\nlistings: {self.listings}'
