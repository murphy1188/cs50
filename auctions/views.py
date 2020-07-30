from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

import datetime

from .models import User, Listing, Comment, Category, Bid, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True)
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

def new_listing(request):
    categories = Category.objects.all().order_by('category_name')
    currentUser = request.user.id
    if request.method == "POST":
        if not request.POST["title"]:
            messages.error(request, "Please enter a title.")
        if not request.POST["price"]:
            messages.error(request, "Please enter a starting price.")
        if not request.POST["details"]:
            messages.error(request, "Please enter listing details.")
        if not request.POST.get("category"):
            messages.error(request, "Please select a category.")
        else:
            listing = Listing.objects.create(title=request.POST["title"],
                startPrice=request.POST["price"],
                details=request.POST["details"],
                image=request.POST["image"],
                category=Category.objects.get(pk=request.POST["category"]),
                created=datetime.datetime.now().strftime("%Y-%m-%d"),
                created_by=User.objects.get(pk=currentUser))
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    return render(request, "auctions/new_listing.html", {
        "categories": categories
    })

def listing(request, listing_id):
    currentUser = request.user.id
    listing = Listing.objects.get(pk=listing_id)
    watchObj = listing.listingwatch.filter(watchUser_id = currentUser)
    bids = Bid.objects.filter(bid_listing = listing)

    if len(watchObj) == 1:
        watching = watchObj[0]
    else: 
        watching = listing.listingwatch.filter(watchUser_id = currentUser)
    comments = listing.comments.filter(listing_id = listing_id)
    try:
        if request.method == "POST":
            if request.POST["action"] == "Close Listing":
                listing.active = False
                listing.save()
                return HttpResponseRedirect(reverse("index"))

            if request.POST["action"] == "Place Bid":
                if not request.POST["bid"]:
                    messages.error(request, "Please enter a bid")
                    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
                bid_price = float(request.POST["bid"])
                if len(bids) == 0: 
                    if bid_price >= listing.startPrice:
                        Bid.objects.create(bid_amt=bid_price, bidder=User.objects.get(pk=currentUser), bid_listing=listing)
                        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
                    else:
                        messages.error(request, "Bid must be equal to or greater than the current price.")

                if len(bids) > 0:
                    if bid_price > listing.listingbids.last().bid_amt:
                        Bid.objects.create(bid_amt=bid_price, bidder=User.objects.get(pk=currentUser), bid_listing=listing)
                        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
                    else:
                        messages.error(request, "Bid must be higher than the current price.")

            if request.POST["action"] == "Add Comment":
                newComment = request.POST["comment"]
                Comment.objects.create(commenter=request.user,
                    comment=request.POST["comment"],
                    listing=listing,
                    date=datetime.datetime.now().strftime("%Y-%m-%d"))
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

            if request.POST["action"] == "Add To Watchlist":
                Watchlist.objects.create(watchUser=request.user,
                    watchedListing=listing)
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
            
            if request.POST["action"] == "Remove From Watchlist":
                watchlistid = request.POST["watchlistID"]
                Watchlist.objects.get(pk=watchlistid).delete()
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
                
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "onWatchlist": watching,
            "bids": bids,
        })   
    except Listing.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))

def category(request, category):
    try:
        category = Category.objects.get(category_name=category)
        listings = category.listings.filter(active=True)
        return render(request, "auctions/category.html", {
            "category": category,
            "listings": listings
        })
    except Category.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all().order_by('category_name')
    })

def watchlist(request):
    watchlist = Watchlist.objects.filter(watchUser=request.user)
    if request.method == "POST": 
        if request.POST["action"] == "Remove From Watchlist":
            watchlistid = request.POST["watchlistID"]
            Watchlist.objects.get(pk=watchlistid).delete()
            return render(request, "auctions/watchlist.html", {
                "watchlist": watchlist})
   
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist})

def closed(request):
    return render(request, "auctions/closed.html", {
        "listings": Listing.objects.filter(active=False)
    })
