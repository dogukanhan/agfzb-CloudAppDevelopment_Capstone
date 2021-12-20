from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from . import restapis
from . import models

logger = logging.getLogger(__name__)


def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)


def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/djangoapp/')
        else:
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)


def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('/djangoapp')


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))

        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("/djangoapp/")
        else:
            return render(request, 'djangoapp/registration.html', context)


def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = 'https://45bd1a82.eu-gb.apigw.appdomain.cloud/dealerships/dealers'
        context = {"dealerships": restapis.get_dealers_from_cf(url)}
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = 'https://45bd1a82.eu-gb.apigw.appdomain.cloud/reviews/get-review?dealerId={0}'.format(dealer_id)
        print("Going for")
        print(url)
        context = {"reviews": restapis.get_dealer_reviews_by_id_from_cf(url, dealer_id)}
        return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, dealer_id):
    if request.method == "GET":
        context = {
            "cars": models.CarModel.objects.all(),
            "dealerId": dealer_id,
        }
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        if request.user.is_authenticated:
            form = request.POST
            review = {
                "name": request.user.first_name + ' ' + request.user.last_name + '(' + request.user.username + ')',
                "dealership": dealer_id,
                "review": form["content"],
                "purchase": form.get("purchasecheck") == "on",
            }
            if form.get("purchasecheck"):
                review["purchaseDate"] = form.get("purchasedate")
                car = models.CarModel.objects.get(pk=form["car"])
                review["carMake"] = car.carmake.name
                review["carModel"] = car.name
                review["year"] = car.year.strftime("%Y")
            json_payload = {"review": review}
            print(json_payload)
            url = "https://45bd1a82.eu-gb.apigw.appdomain.cloud/reviews/add-review"
            restapis.post_request(url, json_payload, dealerId=dealer_id)
            print(json_payload)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            return redirect("/djangoapp/login")
