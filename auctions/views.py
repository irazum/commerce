from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

categories = ['other', 'Fashion', 'Toys', 'Electronics', 'Home']


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        # записать данные в таблицу listings
        # перенаправить на страницу созданного listing-элемента
        l = Listings(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            picture=request.POST.get("pic_url"),
            seller=request.user
        )
        l.save()
        # пробуем создать новую ставку
        try:
            b = Bids(cost=request.POST.get("start_cost"))
            b.save()
        # если ставка с таким значением уже существует
        except IntegrityError:
            b = Bids.objects.filter(cost=request.POST.get("start_cost")).first()
            print(b)
        finally:
            b.users.add(request.user)
            b.listings.add(l)

        return HttpResponseRedirect(reverse("index"))

    if request.user.is_authenticated:
        return render(request, "auctions/create_listing.html", {
            "categories": Categories.objects.all()
        })

    else:
        return HttpResponseRedirect(reverse("login"))