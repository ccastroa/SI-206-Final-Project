import secrets
import json
import requests
import csv
import sqlite3
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.graph_objs as go
import pandas as pd
import numpy as np

class Restaurant:
    def __init__(self, name, Id, lat, lng, street, city, zip_code):
        self.name = name
        self.Id = Id
        self.lat = lat
        self.lng = lng
        self.street = street
        self.city = city
        self.zip_code = zip_code

class Review(Restaurant):
    def __init__(self, rating, text):
        super().__init__(Id)
        self.rating = ratign
        self.text = text

    def __str__(self):
        return "{}, {}".format(self.rating, self.text)

class Veggie:
    def __init__(self):
        self.DBNAME = 'Restaurants.db'
        self.FOODCSV = 'vegetarian_restaurants_US_datafiniti.csv'
        self.fipscsv = 'fips_codes_website.csv'
        self.FASTFOODCSV = 'FastFoodRestaurants.csv'
        try:
            self.conn = sqlite3.connect(self.DBNAME)
            self.cur = self.conn.cursor()
            self.init_db()
            self.add_veg_food_list()
            self.add_fast_food_list()
            self.conn.close()
        except:
            print("Error occurred")

    def init_db(self):
        statement = '''DROP TABLE IF EXISTS 'Veg'; '''
        self.cur.execute(statement)
        self.conn.commit()

        statement = '''
        CREATE TABLE IF NOT EXISTS 'Veg' (
          'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
          "Name" TEXT NOT NULL,
          "Address" TEXT NOT NULL,
          "City" TEXT NOT NULL,
          'State' TEXT NOT NULL,
          'Zipcode' INTEGER NOT NULL,
          'Country' TEXT NOT NULL,
          'Latitude' TEXT NOT NULL,
          "Longitude" TEXT NOT NULL); '''
        self.cur.execute(statement)
        self.conn.commit()

        statement = '''DROP TABLE IF EXISTS 'FastFood'; '''
        self.cur.execute(statement)
        self.conn.commit()

        statement = '''
        CREATE TABLE IF NOT EXISTS 'FastFood' (
          'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
          "Name" TEXT NOT NULL,
          "Address" TEXT NOT NULL,
          "City" TEXT NOT NULL,
          'State' TEXT NOT NULL,
          'Zipcode' INTEGER NOT NULL,
          'Country' TEXT NOT NULL,
          'Latitude' TEXT NOT NULL,
          "Longitude" TEXT NOT NULL); '''
        self.cur.execute(statement)
        self.conn.commit()

    def add_veg_food_list(self):
        foodcsv = open(self.FOODCSV, "r")
        foodinsplist = csv.reader(foodcsv)
        for restaurant in foodinsplist:
            insertion = (None, restaurant[20], restaurant[0], restaurant[2], restaurant[25],
            restaurant[23], restaurant[4], restaurant[15], restaurant[17])
            statement = '''
            INSERT INTO "Veg"
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            self.cur.execute(statement, insertion)
            self.conn.commit()
        foodcsv.close()

    def add_fast_food_list(self):
        foodcsv = open(self.FASTFOODCSV, "r")
        foodinsplist = csv.reader(foodcsv)
        for restaurant in foodinsplist:
            insertion = (None, restaurant[6], restaurant[0], restaurant[1], restaurant[8],
            restaurant[7], restaurant[2], restaurant[4], restaurant[5])
            statement = '''
            INSERT INTO "FastFood"
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            self.cur.execute(statement, insertion)
            self.conn.commit()
        foodcsv.close()

    def process_restaurants(self, cityname):
        self.conn = sqlite3.connect(self.DBNAME)
        self.cur = self.conn.cursor()
        restaurants = """
        SELECT Name, Address, City, State, Zipcode
        FROM Veg
        WHERE Veg.City = '{}' """.format(cityname)
        resss = self.cur.execute(restaurants).fetchall()
        self.conn.close()
        return resss

    def process_fast_food_restaurants(self, cityname):
        self.conn = sqlite3.connect(self.DBNAME)
        self.cur = self.conn.cursor()
        restaurants = """
        SELECT Name, Address, City, State, Zipcode
        FROM FastFood
        WHERE FastFood.City = '{}' """.format(cityname)
        resss = self.cur.execute(restaurants).fetchall()
        self.conn.close()
        return resss

    def process_country_res(self):
        self.conn = sqlite3.connect(self.DBNAME)
        self.cur = self.conn.cursor()
        restaurants = """
        SELECT DISTINCT(State) as States, COUNT(State) as StateCount
        FROM Veg
        GROUP BY State """
        cities = self.cur.execute(restaurants).fetchall()
        self.conn.close()
        stateByVeg = []
        stateList = []
        countList = []
        for i in cities:
            if (i[0] == ''):
                continue

            stateList.append(i[0])
            countList.append(i[1])

        stateByVeg.append(stateList)
        stateByVeg.append(countList)
        return stateByVeg

    def process_fast_country(self):
        self.conn = sqlite3.connect(self.DBNAME)
        self.cur = self.conn.cursor()
        restaurants = """
        SELECT DISTINCT(State) as States, COUNT(State) as StateCount
        FROM FastFood
        GROUP BY State """
        cities = self.cur.execute(restaurants).fetchall()
        self.conn.close()
        stateByFast = []
        stateList = []
        countList = []
        for i in cities:
            if (i[0] == ''):
                continue

            stateList.append(i[0])
            countList.append(i[1])

        stateByFast.append(stateList)
        stateByFast.append(countList)
        return stateByFast

    def process_city_veg_chart(self, city):
        self.conn = sqlite3.connect(self.DBNAME)
        self.cur = self.conn.cursor()
        restaurants = """
        SELECT DISTINCT(Zipcode), COUNT(City)
        FROM Veg
        WHERE Veg.City = '{}'
        GROUP BY Zipcode """.format(city)
        cities = self.cur.execute(restaurants).fetchall()
        self.conn.close()
        stateByVegs = []
        zipList = []
        countList = []
        for i in cities:
            if (i[0] == ''):
                continue

            zipList.append(str(i[0]))
            countList.append(i[1])
        stateByVegs.append(zipList)
        stateByVegs.append(countList)
        return stateByVegs

class Cache:
    def __init__(self):
        self.cache = []
        self.size = 0
    def add(self, restaurant):
        if self.size <= 500 :
            self.cache.insert(0, restaurant)
            self.size += 1
        else:
            self.cache.pop()
            self.cache.insert(0, restaurant)

class RestaurauntInfo:
    def __init__(self, name, directions, rating):
        self.name = name
        self.directions = directions
        self.rating = rating

def get_id_for_location(place,location):
    categories = {"alias": "vegetarian", "title": "Vegetarian", "parents": ["restaurants"]}
    response = requests.get("https://api.yelp.com/v3/businesses/search",
    headers = {"Authorization" : 'Bearer %s' % secrets.y_api_key},
    params = {'term': place, 'location' : location})
    ids = {}
    restaurants = json.loads(response.text)["businesses"]
    for restaurant in restaurants:
        ids[restaurant['name']] = restaurant['id']
        ids['lat'] = restaurant['coordinates']['latitude']
        ids['lng'] = restaurant['coordinates']['longitude']
        ids['rating'] = restaurant['rating']
    return ids

def get_reviews(Id):
    response = requests.get('https://api.yelp.com/v3/businesses/'+ Id + '/reviews',
    headers = {"Authorization" : 'Bearer %s' % secrets.y_api_key},
    params = {'apikey': secrets.y_api_key})
    reviews = json.loads(response.text)["reviews"]
    review_lst = []
    for review in reviews:
        date = review['time_created']
        rating = review['rating']
        text = review['text']
        review_lst.append((date, rating, text))
    return review_lst

#######################
      # GRAPHS #
#######################

def display_one_map(place, lat, lng, city):
    data = Data([
    Scattermapbox(
        lat = [str(lat)],
        lon = [str(lng)],
        mode='markers',
        marker=
        Marker(
            size=14),
        text = city,)])
    layout = Layout(
        title='{}'.format(place),
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=secrets.mapbox_access_token,
            bearing=0,
            center=dict(
                lat=lat,
                lon=lng),
            pitch=0,
            zoom=5))
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename = city + "Mapbox")

class Progam:
    def __init__(self):
        self.city = None
        self.exit = False
        self.cache = Cache()
        self.table = Veggie()
        self.reslst = []
        self.resnum = None
        self.name = None
        self.address = None
        self.state = None
        self.zipcode = None
        self.id = None
        self.revlist = []
        self.distinctcities = []
        while self.exit is False:
            self.running()

    def cityname(self):
        self.city = input("Enter a city: ").rstrip()

    def restaurant_address(self):
        fast_or_veg = input("Enter 'fast' for Fast Food or 'veg' for Vegan/Vegetarian restaurants: ")
        if fast_or_veg == 'veg':
            self.reslst = self.table.process_restaurants(self.city)
        elif fast_or_veg == 'fast':
            self.reslst = self.table.process_fast_food_restaurants(self.city)
        else:
            fast_or_veg = input("Enter 'fast' or 'veg' for restaurants: ")
        counter = 1
        for restaurant in self.reslst:
            print (str(counter) + ': ' + str(restaurant[0]) + ' ' + str(restaurant[1]) + ' ' + str(restaurant[2]) + ', ' + str(restaurant[3]) + ', ' + str(restaurant[4]))
            counter+=1
        self.resnum = int(input("Select a number to select a restaurant: "))-1
        if self.resnum > len(self.reslst):
            self.resnum = int(input("Select a number within the list to select a restaurant: "))-1
            self.name = self.reslst[self.resnum][0]
            self.address = self.reslst[self.resnum][1]
            self.city = self.reslst[self.resnum][2]
            self.state = self.reslst[self.resnum][3]
            self.zipcode = self.reslst[self.resnum][4]
            return self.name, self.address, self.city, self. state, self.zipcode
        else:
            self.name = self.reslst[self.resnum][0]
            self.address = self.reslst[self.resnum][1]
            self.city = self.reslst[self.resnum][2]
            self.state = self.reslst[self.resnum][3]
            self.zipcode = self.reslst[self.resnum][4]
            return self.name, self.address, self.city, self. state, self.zipcode

    def restaurant_id(self):
        fulladdress = self.address + ' ' + self.city + ', ' + self.state + ' ' + str(self.zipcode)
        ids = get_id_for_location(self.name, fulladdress)
        self.id = ids[self.name]
        self.lat = ids['lat']
        self.lng = ids['lng']
        self.averagemovierating = ids['rating']
        return self.id, self.lat, self.lng, self.averagemovierating

    def restaurant_reviews(self):
        self.revlist = get_reviews(self.id)
        self.ratinglst = []
        self.reviewlst = []
        for i in self.revlist:
            print(str(i[0]) + ', Rating: ' + str(i[1]) + ', ' + str(i[2] ))
            self.ratinglst.append(i[0])
            self.reviewlst.append(i[1])
        self.cachereviews = self.cache.add(Restaurant(self.name, self.id, self.lat, self.lng, self.address, self.city, self.zipcode))

    def bar_num_chart(self):
        trace1 = go.Bar(
        x=self.table.process_country_res()[0],
        y=self.table.process_country_res()[1],
        name='Vegan and Vegetarian Count')
        trace2 = go.Bar(
        x=self.table.process_fast_country()[0],
        y=self.table.process_fast_country()[1],
        name='Fast Food Count')
        data = [trace1, trace2]
        layout = go.Layout(
        title = 'Vegan & Vegetarian Vs Fast Food Count in the US by State',
        barmode='group')
        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename='grouped-bar')

    def pie_chart(self):
        trace = go.Scatter(
        x = self.table.process_city_veg_chart(self.city)[0],
        y = self.table.process_city_veg_chart(self.city)[1]
)
        data = [trace]
        py.plot(data, filename='basic-line')

    def rating_chart(self):
        trace = go.Table(
        header=dict(values=['TimeStamp', 'Restaurant Rating'],
                    line = dict(color='#7D7F80'),
                    fill = dict(color='#a1c3d1'),
                    align = ['left'] * 5),
        cells=dict(values=[[self.ratinglst],
                           [self.reviewlst]],
                   line = dict(color='#7D7F80'),
                   fill = dict(color='#EDFAFF'),
                   align = ['left'] * 5))

        layout = dict(width=500, height=300)
        data = [trace]
        fig = dict(data=data, layout=layout)
        py.plot(fig, filename = 'styled_table')

    def running(self):
        self.commandlist = ['city', 'review', 'map', 'rating', 'city zip', 'us res', 'help', 'exit']
        self.graphs = input("Enter command or 'help' for more information: ").rstrip().lower()
        if self.graphs in self.commandlist:
            while True:
                if self.graphs == 'city':
                    self.cityname()
                    self.restaurant_address()
                    self.restaurant_id()
                    self.graphs = input("Enter command or 'help' for more information: ").rstrip().lower()

                elif self.graphs == 'review':
                    self.restaurant_reviews()
                    self.graphs = input("Enter command or 'help' for more information: ").rstrip().lower()

                elif self.graphs == 'map':
                    self.single_point_map = display_one_map(self.name, self.lat, self.lng, self.city)
                    self.graphs = input("Enter command or 'help' for more information: ").rstrip().lower()

                elif self.graphs == 'rating':
                    self.rating_chart()
                    self.graphs = input("Enter command or 'help' for more information: ").rstrip().lower()

                elif self.graphs == 'city zip':
                    self.pie_chart()
                    self.graphs = input("Enter command or 'help' for more information: ").rstrip().lower()

                elif self.graphs == 'us res':
                    self.bar_num_chart()
                    self.graphs = input("Enter command or 'help' for more information: ").rstrip().lower()

                elif self.graphs == 'exit':
                    exit()

                elif self.graphs == 'help':
                    print("""
                    city \n
                        available anytime. Use to select a city.\n
                        lists all Vegetarian/Vegan or fast food Restaurants for city selected\n
                        valid inputs: 'city' + name of a city (name capitalized)\n
                    review \n
                        available only if there is an active restaurant results list\n
                        lists three reviews for the restaurant picked\n
                        valid inputs: 'reviews'\n
                    map \n
                        available only if there is an active restaurant results list\n
                        opens up a map of the selected restaurant on a plotly map\n
                        valid inputs: 'map'\n
                    rating \n
                        available only if there is an active set of reviews for selected restaurant\n
                        opens up a table of the selected restaurant's rating and timestamp of rating\n
                        valid inputs: 'rating'\n
                    city zip \n
                        available only if there is an active restaurant results list\n
                        opens up a pie chart of the selected city's Vegan/Vegetarian\n
                        restaurants popularity by zipcode\n
                        valid inputs: 'city zip'\n
                    us res \n
                        available anytime\n
                        opens up a bar graph of all the restaurants sorted by state \n
                        for Vegan/Vegetarian and Fast food restaurants\n
                        valid inputs: 'us res'\n
                    exit \n
                        exits the program\n
                    help \n
                        lists available commands (these instructions)")""")
                    self.graphs = input("Enter command or 'help' for more information: ").rstrip().lower()

        else:
            print("Command not recognized: {}".format(self.graphs))
            self.graphs = input("Enter command or 'help' for more information: ").rstrip().lower()

if __name__ == '__main__':
    Progam()
