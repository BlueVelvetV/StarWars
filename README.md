# StarWars

# Requirements
Install all the necessary requirements from requierements.txt

# Classes
Backend:
    -app.py -> contains the API requests to STAR-WARS-SWAPI to store all the planets information into planets.db and display the data 
    -fill_db.py -> populate the database by cycling on the planets retrieved and storing the information base on the tables defined in models.py
    -models.py -> contains 3 classes for Planets, Climates and Terrains
Frontend:
    -App.js -> get the planets stored in the db and display them

# Run the backend
Make sure the previous db has been deleted -> instance/planets.db
run app.py

# Run the frontend
from start-wars-planet-manager/star-wars-planet-manager-ui -> npm start
