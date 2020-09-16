from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.db.models.functions import Distance
from .models import John, Review, AuthUser
import requests
import json
import time

@ensure_csrf_cookie
def index(request):
    return render(request, "crappermapper/index.html")

def locate(request):
    return render(request, "crappermapper/index.html")

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
            return render(request, "crappermapper/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        users = User.objects.all()
        return render(request, "crappermapper/login.html")

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
            return render(request, "crappermapper/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "crappermapper/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "crappermapper/register.html")

@ensure_csrf_cookie
@login_required
def review(request):
    user = AuthUser.objects.get(id=request.user.id)
    if request.method == "POST":
        data = json.loads(request.body)
        review_text = data.get("review_text", "")
        review_title = data.get("review_title", "")
        rating = data.get("review_rating", "")
        john = John.objects.get(id=data.get("john_id"))

        review = Review(
            user=user,
            rating=rating,
            review_title=review_title,
            review_text=review_text,
            john=john
        )
        review.save()
        
        return JsonResponse({"message": "New review submitted."}, status=201)
    if request.method == "PUT":
        
        data = json.loads(request.body)
        johnID = data.get("john_id", "")
        johnObj = John.objects.get(id=johnID)
        review = Review.objects.get(user=user, john=johnObj)
        review.review_title = data.get("review_title", "")
        review.review_text = data.get("review_text", "")
        review.rating = data.get("review_rating", "")
        review.save()
        return JsonResponse({"message": "Review edit submitted"}, status=201)

def get_data(request, john_location):
    if john_location != 'all':
        johns_data = John.objects.filter(pk=john_location)
        
    if john_location == 'all':
        user_location = Point(float(request.GET.get('lng')), float(request.GET.get('lat')), srid=4326)
        johns_data = John.objects.annotate(distance=Distance("location", user_location)).order_by("distance")[0:20]
    
    johns_list = []

    for john in johns_data:
        reviews = Review.objects.filter(john=john.id)
        review_list = []
        for review in reviews:
            review_item = {
                'reviewID': review.id,
                'username': review.user.username,
                'userID': review.user.id,
                'johnID': review.john.id,
                'rating': review.rating,
                'review_title': review.review_title,
                'review_text': review.review_text,
                'timestamp': review.timestamp.strftime("%b %d %Y, %I:%M %p")
            }
            review_list.append(review_item)
        john_item = {
            'id': john.id,
            'name': john.name,
            'display_name': john.display_name,
            'geometry': {
                'type': 'Point',
                "coordinates": [
                    john.location[1],
                    john.location[0]
                ]
            },
            'place_id': john.place_id,
            'reviews': review_list,
        }
        johns_list.append(john_item)
    return JsonResponse({'data': johns_list})

@login_required
def add_new_john(request):

    if request.method == "POST":
        newLoc = json.loads(request.body)
        lat = newLoc['lat']
        lng = newLoc['lng']
        address = newLoc['address']
        location = fromstr(
            f'POINT({lng} {lat})', srid=4326
        )
        try:
            newJohn = John(
                location=location,
                address=newLoc['address'],
                street_number=newLoc['street_no'],
                street_name=newLoc['street_name'],
                city=newLoc['city'],
                state=newLoc['state'],
                zip_code=newLoc['zip_code'],
                county=newLoc['county'],
                country_code=newLoc['country'],
                display_name=newLoc['address'],
                name='no-name'
            )
            newJohn.save()
            newJohnId = newJohn.id
            return HttpResponse(newJohnId)
        except IntegrityError:
            return HttpResponse('alreadyExists')

    else:
        return JsonResponse({"error": "POST request required"}, status=400)

@login_required
def reverse_geocode(request):

    lat = request.GET.get("lat")
    lng = request.GET.get("lng")

    # opencagedata api key
    key = 'd8d51cf71aff402da255bea910122f1e'
    url = 'https://api.opencagedata.com/geocode/v1/json?q=' + lat + ',' + lng + '&key=' + key
    response = requests.request("GET", url)
    location_data = response.json()
    
    try:
        street_number = location_data['results'][0]['components']['house_number']
    except:
        street_number = 'null'

    try:
        street_name = location_data['results'][0]['components']['road']
    except:
        street_name = 'null'

    try:
        city = location_data['results'][0]['components']['town']
    except:
        city = 'null'

    try:
        state = location_data['results'][0]['components']['state']
    except:
        state = 'null'

    try:
        zip_code = location_data['results'][0]['components']['postcode']
    except:
        zip_code = 'null'

    try:
        county = location_data['results'][0]['components']['county']
    except:
        county = 'null'
    
    try:
        country = location_data['results'][0]['components']['country_code'].upper()
    except:
        country = 'null'

    location = fromstr(
        f'POINT({lng} {lat})', srid=4326
    )
    newJohn = {
        'address': location_data['results'][0]['formatted'],
        'street_number': street_number,
        'street_name': street_name,
        'city': city,
        'state': state,
        'zip_code': zip_code,
        'county': county,
        'country_code': country
    }
    return JsonResponse({'data': newJohn})


