
Data Sources Used:

* Create a yelp app to obtain an api key and client id here:
    https://www.yelp.com/developers/v3/manage_app
    * Yelp Business Search Api:
        https://www.yelp.com/developers/documentation/v3/business_search
    * Yelp Business ID Reviews Api:
        https://www.yelp.com/developers/documentation/v3/business_reviews
* Plotly Api
    https://plot.ly/settings/api (Get API Key here)
    https://plot.ly/settings/mapbox (Get Mapbox access token here)
* Fast Food Restaurants Dataset
    https://www.kaggle.com/datafiniti/fast-food-restaurants (Download)
* Vegetarian and Vegan Restaurants Dataset
    https://www.kaggle.com/datafiniti/vegetarian-vegan-restaurants (Download)



Large Lists:
- my cache function is a list which stores the address data from restaurants selected.

User Guide:
- Begin by running the program with 'python3 proj.py'
- From there, the user can enter one of the following commands: ['city', 'reviews',
    'map', 'rating', 'city bars', 'country bars', 'help', or 'exit']

    Presentation / Help:

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
            lists available commands (these instructions)")
