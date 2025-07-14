from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.db import IntegrityError, models
from django.contrib.auth.models import Group
from .models import *
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.db.models.functions import ACos, Cos, Radians, Sin
from django.db.models import FloatField, F, Func, Value , ExpressionWrapper
from django.db.models.expressions import RawSQL
import requests
import pandas as pd
import json
from haversine import haversine, Unit


    
    

def index(request):
    camper=check_group(request.user)
    facilities = Facility.objects.all().values()
    campsites = Campsite.objects.all()
    
    
    return render(request, "index.html",{'camper' : camper, 'facilities' : facilities , 'campsites' : campsites })
        
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
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["forname"]
        last_name = request.POST["surname"]
        phone = request.POST["phone"]
        dob = request.POST["dob"]
        group = request.POST["usertype"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name = first_name, last_name = last_name, phone = phone, dob = dob)
            user.save()
            group =Group.objects.get(name=group)
            group.user_set.add(user)
            
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        
        
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")

def check_group(user):
    return user.groups.filter(name='camper').exists()

@login_required 
def campadmin(request):
    camper=check_group(request.user)
    facilities = Facility.objects.all().values()
    campsites = Campsite.objects.filter(owner = request.user)
    
    
    return render(request, "campadmin.html",{'camper' : camper, 'facilities' : facilities , 'campsites' : campsites })

def add_campsite(request):

    if request.method == "POST":
        
        
        owner = request.user
        name = request.POST["name"]
        description = request.POST["description"]
        picture = request.POST["picture"]
        address1 = request.POST["address1"]
        address2 = request.POST["address2"]
        town = request.POST["town"]
        county = request.POST["county"]
        postcode = request.POST["postcode"]
        gps = get_coords(request.POST["postcode"])
        latitude = gps[1]
        longitude = gps[0] 
        email = request.POST["email"] 
        phone = request.POST["phone"]        
        facilities = request.POST.getlist("facility_list")
        campsite = Campsite(owner=owner,name=name,description=description,picture=picture,address1=address1,address2=address2,latitude=latitude,longitude=longitude,town=town,county=county,postcode=postcode,email=email,phone=phone)
        campsite.save()
        print(facilities)
        for facility in facilities:
            campsite.facilities.add(facility)
            
        
        
        
        
        return HttpResponseRedirect(reverse("index"))
    
def get_coords(postcode):
    data= requests.get(f"https://api.postcodes.io/postcodes/{postcode}")
    json = data.json()
    if data.status_code == 200:
        gps = [json['result']['longitude'],json['result']['latitude']]
    else:
        gps = [0, 0]
    return gps

def site(request, siteID):
    site = Campsite.objects.get(id=siteID)
    facilities = site.facilities.all()
    camper=check_group(request.user)
    types = Plot.Types.names
    plots = site.plots.all()

    
    '''
    try:
        nearby_campsites = get_nearby_campsites(Campsite.objects.all(), "BS30 6JS", 90)
        
        for campsite in nearby_campsites:
            print(campsite.name)
    except Exception as e:
        print(f"Error: {e}")
    '''
    return render(request, "site.html", {'camper' : camper, "site":site, "facilities":facilities,"types":types, "plots":plots})

def add_plot(request):
    if request.method == "POST":
        id = request.POST["id"]
        campsite = Campsite.objects.get(id=id)
        name = request.POST["name"]
        type = request.POST["type"]
        power = request.POST["power"]
        capacity = request.POST["capacity"]
        length = request.POST["length"]
        width = request.POST["width"]
        price =request.POST["price"]
        plot = Plot(campsite=campsite,name=name,type=type,power=power,capacity=capacity,length=length,width=width,price=price)
        plot.save()
        
        return HttpResponseRedirect(reverse('site', kwargs={'siteID':id}))
def delete_plot(request, plotID):     
    plot = Plot.objects.get(id=plotID)
    site = Campsite.objects.get(id=plot.campsite.id)
    facilities = site.facilities.all()
    camper= check_group(request.user)
    types = Plot.Types.names
    plots = site.plots.all()
    plot.delete()
      
    return render(request, "site.html", {'camper' : camper, "site":site, "facilities":facilities,"types":types, "plots":plots})

def close_site(request, siteID):
    site = Campsite.objects.get(id=siteID)
    site.delete()
    
    return HttpResponseRedirect(reverse('index'))

def book (request, type, id):
    

    if request.method == "GET":
        
        try:
            if type == "site":
                site = Campsite.objects.get(id=id)
                plot = site.plots.all()
                selection = plot[0]
            elif type == "plot":
                selection=plot= Plot.objects.get(id=id)
                site = plot.campsite
                plot = site.plots.all()         
        except Exception as e:
            print(f"Error : {e}")
            camper=check_group(request.user)
            facilities = Facility.objects.all().values()
            campsites = Campsite.objects.all()
    
            return render(request, "index.html",{'camper' : camper, 'facilities' : facilities , 'campsites' : campsites })    
        
        plots = []
        for plot in plot:
            plots.append(plot)
       
                
        return render(request, "book.html", {'site': site, 'type':type, 'plots':plots, 'selection':selection})
    elif request.method == "POST":
        
        bookings = check_bookings(request.POST["checkin"],request.POST["checkout"],request.POST["plot"])
        
        if not bookings :
            user=User.objects.get(username= request.user)
            plot=Plot.objects.get(id=request.POST["plot"])
            arrival = request.POST["checkin"]
            checkout = request.POST["checkout"]
            days = date_diff(arrival,checkout)
            people = request.POST["people"]
            notes = request.POST["notes"]
            cost = days * plot.price
            booking = Booking(user=user,plot=plot,arrival=arrival,checkout=checkout,people=people,notes=notes, cost=cost)
            booking.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            #TODO return user to booking page with message that plot is booked
            for booking in bookings: 
                site = Campsite.objects.get(id=id)
                plot = site.plots.all()
                plots = []
                for plot in plot:
                    plots.append(plot)               
            return render(request, "book.html", {'site': site, 'type':type, 'plots':plots, 'bookings': bookings})

def date_diff (start, finish):
   ## TO DO add validation for dates, check avalability, add in JS??
    a = start.rsplit("-")
    b = finish.rsplit("-")
    difference = date(int(b[0]),int(b[1]),int(b[2])) - date(int(a[0]),int(a[1]),int(a[2]))
    return difference.days

def check_bookings(start,finish, plotID):
        
        plot=Plot.objects.get(id=plotID)
       
        #arrival plus 1 variable
        a = pd.Timestamp(start)+pd.Timedelta(days=1)          
        #checkout - 1 variable
        o = pd.Timestamp(finish) - pd.Timedelta(days=1)
        list = Booking.objects.filter(arrival__range=(start, o), plot=plot).values() | Booking.objects.filter(checkout__range=(a, finish), plot=plot).values()
        return list 

def view_bookings(request, siteID):
    site = Campsite.objects.get(id=siteID)
    plot = site.plots.all()
    plots = []
    for plot in plot:
        plots.append(plot) 
    bookings = Booking.objects.filter(plot__in=plots)
    return render(request, "view_bookings.html", {"site":site, "bookings":bookings})

def facility(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        name = name.title()      
        if Facility.objects.filter(name=name).exists():
            return JsonResponse({"message": "Facility already exists"})
        else:
            facility =Facility(name=name)
            facility.save()
            return JsonResponse({"message": "Facility added!"}, status=201)

def search(request):
    search = f"Campsites within {request.POST["distance"]}KM's of {request.POST["postcode"]}"
    camper=check_group(request.user)
    facilities = Facility.objects.all().values()
    plotDict = {}
    campsites = Campsite.objects.exclude(owner = request.user)
    try:
        campsites = get_nearby_campsites(campsites, request.POST["postcode"], int(request.POST["distance"]))
        

        for campsite in campsites:
            plotDict[campsite.name] = []
            plots = campsite.plots.all()
            if request.POST["arrive"] !="" and request.POST["depart"] != "":
                
                for plot in plots:
                    plot.available = True
                    if check_bookings(request.POST["arrive"], request.POST["depart"], plot.id):
                        plot.available = False
                    else:
                        plotDict[campsite.name].append(plot.name)    
                    
            
        if request.POST["arrive"] !="" and request.POST["depart"] != "":
            search = search + f" with availability between {request.POST["arrive"]} and {request.POST["depart"]}"
        
    except Exception as e:
        print(f"Error: {e}")
     
    
    return render(request, "index.html",{'camper' : camper, 'facilities' : facilities , 'campsites' : campsites , 'distance' : 'True', 'plots' :plotDict, 'search':search})

def get_nearby_campsites(queryset, postcode, distance_km):
    gps = get_coords(postcode)
    list = []

    for location in queryset:
        distance = haversine((gps[1],gps[0]),(location.latitude,location.longitude),unit=Unit.KILOMETERS)
        location.distance = distance
        if distance < distance_km:
            list.append(location)   
    list.sort(key=lambda loc: loc.distance)

    
    return list
@login_required 
def accountadmin(request):
    message = ""
    if request.method == "POST":
        try:
            user = User.objects.get(id=request.user.id)
            user.email = request.POST["email"]
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.phone = request.POST["phone"]
            user.save()
            message = "Updated succesfully"
        except Exception as e:
            message = f"Upadate unsuccessful error reason - {e}"  
            print(f"Error: {e}")
    else :
        user = User.objects.get(id=request.user.id)

    return render(request, "accountadmin.html", {'user' : user, 'message' : message})
@login_required 
def updatepassword(request):
    # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["old"]
        user = authenticate(request, username=username, password=password)
        message = "Password update failed!!"
        # Check if authentication successful
        if user is not None:
            if request.POST["new1"] == request.POST["new2"]:
                user.set_password(request.POST["new1"])
                user.save()
                message = "Password update Succesful!"
                
        else:
            user = User.objects.get(id=request.user.id)
        
        return render(request, "accountadmin.html", {'user' : user, 'message' : message})
            
   
    