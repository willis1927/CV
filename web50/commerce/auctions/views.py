from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, forms, HiddenInput, widgets
from .models import *
from datetime import datetime

class CategoryForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["category"]
        

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["name","description","category","imageURL"]
        

def index(request):
    if request.method == "POST": 
        category = request.POST["category"]
        categories = CategoryForm(initial={'category': category})     
        return render(request, "auctions/index.html", {"listings" : Listing.objects.filter(category=category), 'categories': categories, 'category': category})
    else:

        return render(request, "auctions/index.html", {"listings" : Listing.objects.filter(active="True"), 'categories': CategoryForm()})


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

@login_required
def new(request):
    if request.POST:
        currentUser = request.user
        name = request.POST["name"]
        description = request.POST["description"]
        category = request.POST["category"]
        bid = Bid(bid=0.00, user=currentUser)
        bid.save()   
        if request.POST["imageURL"] == "":
            imageUrl = "https://t4.ftcdn.net/jpg/04/70/29/97/360_F_470299797_UD0eoVMMSUbHCcNJCdv2t8B2g1GVqYgs.jpg"
        else:
            imageUrl = request.POST["imageURL"] 
        n = Listing(
            owner = currentUser,
            name = name,
            description = description,
            category = category,
            price = bid,
            imageURL = imageUrl,  
        ) 
        n.save()
             
        return HttpResponseRedirect(reverse("index"))
    else:
        
        return render(request, "auctions/new.html", {'form': ListingForm()})
    
    
def listing(request, listingID):
    listing = Listing.objects.get(listingID=listingID)
    comments = Comment.objects.filter(listingID=listingID).order_by("-time").values()
    for comment in comments:    
        comment["user"]= User.objects.get(id=comment["user_id"])
    currentUser = request.user
    watched = False
    try:
        watches = currentUser.watched.all()
        for watch in watches:                
            if watch.listingID == listingID:                  
                watched = True                  
    except:
        pass
       

    data = {    
        "name" : listing.name,
        "description": listing.description,
        "category": listing.category,
        "price": listing.price,
        "imageURL": listing.imageURL
    }
    form = ListingForm(initial=data)
    isOwner = request.user.username == listing.owner.username
    isWinner = currentUser == listing.price.user
    
    return render(request, "auctions/listing.html", {"watched":watched, "listing" :listing, "form":form, "isOwner": isOwner, "isWinner": isWinner, "comments": comments})

@login_required
def amend(request):
    if request.POST:
        name = request.POST["name"]
        description = request.POST["description"]
        category = request.POST["category"]
        if request.POST["imageURL"] == "":
            imageUrl = "https://t4.ftcdn.net/jpg/04/70/29/97/360_F_470299797_UD0eoVMMSUbHCcNJCdv2t8B2g1GVqYgs.jpg"
        else:
            imageUrl = request.POST["imageURL"] 
        listing = Listing.objects.get(listingID=request.POST["listingID"])
        listing.name = name
        listing.description = description
        listing.category = category
        listing.imageURL = imageUrl
        listing.save() 
        return HttpResponseRedirect(reverse("index")) 

@login_required
def watchlist (request):
    currentUser = request.user
    watches = currentUser.watched.all()
    #return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/watch.html", {"listings" : watches})
    
     
@login_required
def watch (request):
    
    listingID = request.POST["listingID"]
    listing = Listing.objects.get(listingID=listingID)
    currentUser = request.user
    listing.watches.add(currentUser)
    return HttpResponseRedirect(reverse("watchlist"))  

@login_required    
def removewatch (request):
    listingID = request.POST["listingID"]
    listing = Listing.objects.get(listingID=listingID)
    currentUser = request.user
    listing.watches.remove(currentUser)
    
    return HttpResponseRedirect(reverse("watchlist"))   

@login_required
def bid (request):  
    listing = Listing.objects.get(pk=request.POST["listingID"])
    currentBid = listing.price.bid
    try:
        newBid = float(request.POST["bid"])     
    except ValueError:
        return render(request, "auctions/index.html", {"listings" : Listing.objects.filter(active="True"), 'categories': CategoryForm(),"message": f"Error - Bid must be numerical!"})
    if newBid > currentBid:
        b = Bid(
            user = request.user,
            bid = newBid
        )
        b.save()
        listing.price = b
        listing.save()        
        return render(request, "auctions/index.html", {"listings" : Listing.objects.filter(active="True"), 'categories': CategoryForm(),"success":True,"message": f"New highest bid for {listing.name} is £{listing.price.bid:0.2f}"})
    else:
        return render(request, "auctions/index.html", {"listings" : Listing.objects.filter(active="True"), 'categories': CategoryForm(),"message": f"Bid must be greater than £{listing.price.bid:0.2f}"})

@login_required
def close(request):
    if request.method == "POST":
        listing = Listing.objects.get(listingID = request.POST["listingID"]) 
        listing.active = False
        listing.save()
        return HttpResponseRedirect(reverse("index")) 
    
def comment(request):
    if request.POST:
        comment = request.POST["comment"]
        listingID = request.POST["listingID"]
        listing = Listing.objects.get(listingID = listingID)
        if comment:
            comment = Comment(listingID=listing, user=request.user ,text=comment)
            comment.save()
        
        print(comment)
    
    return HttpResponseRedirect(reverse("listing",args=(listingID, )))