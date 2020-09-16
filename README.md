CS50W Capstone Project

CrapperMapper

For my capstone project for CS50W, I created a web application called CrapperMapper. The purpose of this application is to provide the user with the closest bathrooms to their current location, along with ratings and reviews for each bathroom in the user's vicinity. This application utilizes Django on the back-end and JavaScript on the front-end to make the user-interface responsive. 

When CrapperMapper is loaded, the user is automatically geolocated and the user's location is displayed on the map. The 20 closest bathroom locations are also loaded and displayed on the map, as well as in a sidebar that the user is able to scroll through. The user can select a bathroom location either by clicking the icon on the map or by clicking the listing for that bathroom in the sidebar. 

User's are able to view reviews for each location from other users, add their own review, edit their review if they have already made a review for that location, and they may also add a new bathroom location if a location does not yet exist in the CrapperMapper database.

models.py - This file contains the models used to store user account information, location information for each bathroom, and review information for each bathroom location.

views.py - This file contains the views used to make api calls for retrieving database information, including bathroom locations, reviews, and user information. This file also contains the view to render login, logout, and register pages, as well and the main index page.

index.html - This file contains the html and JavaScript for the main page of the application, including the map and sidebar to display information for all bathroom locations withing the user's vicinity.

styles.css - This file contains the style information for each page of the application.

crappermapper.js - This file contains additional JavaScript which is not included in the script of the main index.html file.

urls.py - This file contains the url routes for each corresponding view in views.py.

layout.html - This file contains the layout template.

login.html - This file is rendered for the login view. 

register.html - This file is rendered to allow the user to register for an account.



