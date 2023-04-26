from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Bid
from .forms import NewListingForm


def index(request):
    active_listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": active_listings
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
    if request.method == "GET":
        return render(request, "auctions/new_listing.html", {
            "create_form": NewListingForm()
        })
    elif request.method == "POST":
        create_form = NewListingForm(request.POST)
        if create_form.is_valid():
            # Get data from the form
            title = create_form.cleaned_data["title"]
            description = create_form.cleaned_data["description"]
            price = create_form.cleaned_data["price"]
            image_url = create_form.cleaned_data["image_url"]
            category = create_form.cleaned_data["category"]

            # Get the user
            current_user = request.user

            # Create new bid object
            bid = Bid(bid=float(price), user=current_user)

            # Save new bid
            bid.save()

            # Create new listing object
            new_listing = Listing(
                title=title,
                description=description,
                price=bid.bid,
                image_url=image_url,
                category=category,
                owner = current_user
            )

            # Save new listing
            new_listing.save()

            # Redirect to index page
            return HttpResponseRedirect(reverse("index"))
    
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    isListingInWatchlist = request.user in listing.watchlist.all()
    return render(request, "auctions/listing.html", {
        "listing":listing,
        "isListingInWatchList":isListingInWatchlist
    })

def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    current_user = request.user
    listing.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
       
def remove_from_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    current_user = request.user
    listing.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse('listing', args=(listing_id, )))   

def watchlist(request):
    current_user = request.user
    listing_content = current_user.watchlistListing.all()
    return render(request, 'auctions/watchlist.html', {
        "listings": listing_content
    }) 

def bid(request):
    pass  