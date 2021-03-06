from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    # creating html-template parameters depend on GET-data
    # for winlist
    if request.GET.get('winlist'):
        title = 'Win List'
        listings_data = list()
        for listing in Listings.objects.filter(status=False):
            bid = Bids.objects.filter(listing=listing).last()
            if request.user == bid.user:
                listings_data.append({
                    'listing': listing,
                    'max_bid': bid.cost
                })
    # for watchlist, categorylist, mylist and activelist
    else:
        if request.GET.get('watchlist'):
            title = 'Watchlist'
            kwargs = {'watchlist': request.user}
        elif request.GET.get('category'):
            title = request.GET.get('category')
            kwargs = {
                'category': Categories.objects.get(category=title),
                'status': True
            }
        elif request.GET.get('mylist'):
            title = "MyList"
            kwargs = {'seller': request.user}
        else:
            title = 'Active Listings'
            kwargs = {"status": True}

        # make list of dicts of listing and it's max_bid, listing filter depend on GET-data
        listings_data = list()
        for listing in Listings.objects.filter(**kwargs):
            listings_data.append({
                'listing': listing,
                'max_bid': max(Bids.objects.filter(listing=listing).values_list('cost', flat=True))
            })
    return render(request, "auctions/index.html", {
        'listings_data': listings_data,
        'title': title
    })


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
    # Post handler
    if request.method == "POST":
        title = request.POST.get("title", '')
        description = request.POST.get("description", '')
        picture = request.POST.get("pic_url", '')
        category = request.POST.get("category", '')
        cost = request.POST.get("start_cost", '')

        # form-data checking
        if 50>=len(title)>0 and 1000>=len(description)>0 and 9>=len(cost)>0 and (
                len(picture)<=250 and Categories.objects.get(category=category)):
            try:
                cost = int(cost)
            except ValueError:
                return HttpResponseRedirect(reverse('create-listing'))
            # write data in tables listings and bids
            listing = Listings(
                title=title,
                description=description,
                picture=picture,
                seller=request.user,
                category=Categories.objects.get(category=category)
            )
            listing.save()
            Bids(cost=cost, user=request.user, listing=listing).save()
            # ! редактировать: перенаправить на страницу созданного listing-элемента
            return HttpResponseRedirect(reverse("listing", kwargs={'id': listing.pk}))
        else:
            return HttpResponseRedirect(reverse('create-listing'))
    # GET-handler
    if request.user.is_authenticated:
        return render(request, "auctions/create_listing.html", {
            "categories": Categories.objects.all()
        })

    else:
        return HttpResponseRedirect(reverse("login"))


def listing(request, id):
    # check on not exist listing
    try:
        listing = Listings.objects.get(id=id)
        bids = Bids.objects.filter(listing=listing)
    except:
        return HttpResponseRedirect(reverse('index'))
    # POST handler
    if request.method == "POST":
        bid = request.POST.get('bid')
        comment = request.POST.get('comment')
        # authenticated checking
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        # bid handler
        if bid:
            # form-data checking
            if not (9 >= len(bid) > 0):
                return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))
            try:
                bid = int(bid)
            except ValueError:
                return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))
            # bid handler
            if request.user == listing.seller:
                message = "Error! You are the creator of this listing. You can't bid!"
                return HttpResponseRedirect(f"{reverse('listing', kwargs={'id': id})}?message={message}")
            else:
                max_bid = max(i.cost for i in bids)
                if bid > max_bid or (len(bids) == 1 and bid >= max_bid):
                    Bids(cost=bid, user=request.user, listing=listing).save()
                    return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))
                else:
                    message = 'Error. You should put the bid more than a previous bid!'
                    response = HttpResponseRedirect(f"{reverse('listing', kwargs={'id': id})}?message={message}")
                    return response
        elif comment:
            # form-data checking
            if not (2000 >= len(comment) >= 0):
                return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))
            # comment handler
            Comments(comment=comment, user=request.user, listing=listing).save()
            return HttpResponseRedirect(f"{reverse('listing', kwargs={'id': id})}#bottom")
    # GET handler
    if request.user.is_authenticated:
        message = request.GET.get('message', '')
        watchlist = request.GET.get('watchlist')
        close = request.GET.get('close')
        delete = request.GET.get('delete')
        # watchlist handler
        if watchlist:
            watchlist = int(watchlist)
            if watchlist == 1:
                listing.watchlist.add(request.user)
            else:
                listing.watchlist.remove(request.user)
            return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))
        # listing status handler
        elif close:
            listing.status = False
            listing.save()
            return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))
        # listing delete request from seller handler
        elif delete:
            listing.delete()
            return HttpResponseRedirect(reverse('index'))
        # message handler
        elif message:
            pass
        else:
            message = f'{len(bids)} bid(s) so far. '
            if request.user == listing.seller:
                message += "You are the creator of this listing"
            elif request.user == bids[len(bids)-1].user:
                message += "Your bid is the current bid"
            else:
                message += "You can place a bid more than current value or current value if it is 1 bid yet"
    # user is not authenticated
    else:
        message = "Please, LOG IN to access for all abilities of the site!"
    # GET request
    return render(request, "auctions/listing.html", {
        'listing': listing,
        'bids': bids,
        'comments': Comments.objects.filter(listing=listing),
        'message': message,
        'watchlist_users': listing.watchlist.all()
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Categories.objects.all()
    })

