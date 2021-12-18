from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='Audi')
    description = models.CharField(null=False, max_length=300, default='Audi cars are aight')

    def __str__(self):
        return 'Name:' + self.name + ',' + \
               'Description:' + self.description


class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    OTHERS = 'others'
    CAR_CHOICES = [(SEDAN, "Sedan"), (SUV, 'SUV'), (WAGON, 'Wagon'), (OTHERS, 'Others')]
    carmake = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default='BMW E34')
    dealerid = models.IntegerField(null=True)
    cartype = models.CharField(null=False, max_length=20, choices=CAR_CHOICES, default=SEDAN)
    year = models.DateField(null=True)

    def __str__(self):
        return 'Name ' + self.name


class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip
        self.idx = 0

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:
    def __init__(self, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year, sentiment):
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment

    def __str__(self):
        return "Review: " + self.review
