from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Bid, Comment
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
        categories = Category.objects.all()
        return render(request, "auctions/new_listing.html", {
            "create_form": NewListingForm(),
            "categories": categories
        })
    elif request.method == "POST":
        create_form = NewListingForm(request.POST)
        
        if create_form.is_valid():
            # Get data from the form
            title = create_form.cleaned_data["title"]
            description = create_form.cleaned_data["description"]
            starting_bid = create_form.cleaned_data["starting_bid"]
            image_url = create_form.cleaned_data["image_url"]
            category = create_form.cleaned_data["category"]
            current_user = request.user

            # Create new bid object
            bid = Bid(bid=float(starting_bid), user=current_user)
            bid.save()

            # Create new listing object
            new_listing = Listing(
                title=title,
                description=description,
                starting_bid=bid,
                image_url=image_url,
                category=category,
                owner = current_user
            )
            new_listing.save()

            # Redirect to index page
            return HttpResponseRedirect(reverse("index"))
    
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    isListingInWatchlist = request.user in listing.watchlist.all()
    isOwner = request.user.username == listing.owner.username
    return render(request, "auctions/listing.html", {
        "listing":listing,
        "isListingInWatchList":isListingInWatchlist,
        "isOwner": isOwner,

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

def new_bid(request, listing_id):
    new_bid = request.POST.get('new_bid')
    listing = Listing.objects.get(pk=listing_id)
    current_user = request.user
    isListingInWatchList = request.user in listing.watchlist.all()
    isOwner = request.user.username == listing.owner.username
   
    if int(new_bid) > listing.starting_bid.bid:
        updated_bid = Bid(bid = int(new_bid), user=current_user)
        updated_bid.save()
        listing.bid_counter += 1
        listing.starting_bid = updated_bid
        listing.save()
        return render(request, 'auctions/listing.html', {
            "listing": listing,
            "message": "Bid successful!",
            "updated": True,
            "isListingInWatchList": isListingInWatchList,
            "isOwner": isOwner,
            
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Please submit a valid bid.",
            "updated": False,
            "isListingInWatchList": isListingInWatchList,
            "isOwner": isOwner,
        })

def new_comment(request, listing_id):
    new_comment = request.POST.get('new_comment')
    listing = Listing.objects.get(pk=listing_id)
    current_user = request.user
    isListingInWatchList = request.user in listing.watchlist.all()
    comments = Comment.objects.filter(listing = listing)

    listing_comment = Comment(
        author = current_user,
        text = new_comment,
        listing = listing
    )
    listing_comment.save()
    return render(request, 'auctions/listing.html', {
        "listing": listing,
        "user": current_user,
        "isListingInWatchList": isListingInWatchList,
        "comments": comments
    })

def close_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.is_active = False
    listing.save()
    isOwner = request.user.username == listing.owner.username
    isListingInWatchList = request.user in listing.watchlist.all()
    return render(request, 'auctions/listing.html', {
        "listing": listing,
        "isListingInWatchList": isListingInWatchList,
        "isOwner": isOwner,
        "updated": True,
        "message": "Congratulations"
    })