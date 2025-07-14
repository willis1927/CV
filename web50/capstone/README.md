My web app is a campsite management and booking system built using Python, Django, Html, CSS & JS.

Distinctiveness and Complexity:

I believe my application satisfies this criteria as in addition to the basic functionalities of the apps built in other projects it uses Django user groups to distinguish between campers and campsite owners. In addition to this functionality the app also offers a search function that returns available campsites within a date range and also within a user defined radius of KMs. The app also offers user the ability to manage their account and update their password while logged in. Using the Django groups allows the site to serve 2 types of users offering different functionality depending on the account logged in from the same platform, validation has been built in to the app to prevent users accessing areas of the app or performing functions that should not be available to them. 

Application Contents & How to Run:

My application contains the standard files created by Django when creating a web app, to run the app you should navigate into the capstone folder and run in the terminal using the command "python manage.py runserver 0.0.0.0:8000", this will launch the app/server and then navigating to xxx.xxx.xxx.xxx:8000 in a web browser replace the x's with the ip address of the machine hosting the server. Inside the camping folder are all the files required to run the web app, the key folders being static which contains js & css files that are used from different parts of the application and also an Icon file that is used in the browser toolbar. The templates folder contains all the page templates used within the app. The urls.py file lists all url roots that the application uses and references which functions to run from the views.py file.

In order to run the web application you must ensure you have installed the below libraries:

Pandas

Haversine

Application Description : 

I created a web application that would serve as a booking site for Campsites in the UK. I created user groups in Django for campers and campsites as I wanted to prevent campers from being able to create or edit campsites and equally decided that campsites should not be able to book plots at another campsite. The user type is selected by the user when creating an account and this dictates what pages they can view and functionality that they have. When a campsite account is created they are able to create multiple sites and each site can also have multiple plots.

Campsites are able to select what facilities they offer from a list that is populated from all current facilities across the platform and also add additional facilities if they offer something not currently in the list. When adding a new facility there is validation in place to prevent duplicate facilities being created. In addition to selecting what facilities there site offers a campsite owner also adds a description, location & contact details and also a picture. If no picture is provided a default picture is used in its place. The postcode provided is passed to the postcodes.io API which returns the Longitude and Latitude to be used when a user is searching. Once a campsite has been created the owner will then create plots that campers can book, these can be selected as various types such as tent or caravan, if power is offered, maximum occupancy, the size of the pitch and also a price per night. Once a campsite has plots campers are able to book the plot via a booking form that checks if the plot is currently booked over the requested dates and if a booking exists an error message is returned instead of making the booking.

Campsite owners are able to view all campsites that that they manage and when viewing a site they are able to add more plots, view all bookings and delete plots, they are also able to delete a campsite and doing so deletes all plots in that campsite, users are prompted with a warning before doing so.

Campers are able to search for campsites based on proximity to a postcode in kilometres, this was the largest challenge I face when building the app as SQLlite is that it does not offer functionality to calculate distances between to known points. To solve this I used the Haversine library and formula as this can be used to calculate the distances between 2 points on a sphere given their coordinates. When a user runs the search they provide a postcode and a distance that they would like to find campsites within. The postcode is converted to Lon & lat using the API and then the distances between the points are calculated and appended to the records in the database, a filter is then applied to only return postcodes within the desired distance. Campers are also able to include a date range in there search which will give the user a list of plots that are available in their date range. This achieved using the same function that is used when a booking is made which checks for bookings between two dates and only returns plots without bookings.

User who are not logged in are only able to search & view sites but can't make any bookings. Once a user is logged in they are able to manage their account via My Account where they can update contact details and change their password.

There were many other functions that I would have liked to implement into this project such as a review/comment system but it fell outside the scope of the project, if this were a real life application I would look to implement these as part of future updates once the site was full operational.