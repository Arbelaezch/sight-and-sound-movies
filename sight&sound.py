from ast import Num
from bs4 import BeautifulSoup
import requests
from flask import Flask, redirect, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
Bootstrap(app)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/sight-and-sound.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# class Movie(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	title = db.Column(db.String(80), nullable=False)
# 	director = db.Column(db.String(50), nullable=True)
# 	country = db.Column(db.String(20), nullable=True)
# 	year = db.Column(db.String(4), nullable=True)
# 	synopsis = db.Column(db.String(300), nullable=True)
# 	img_url = db.Column(db.String(300), nullable=True) 
# 	movie_url = db.Column(db.String(300), nullable=True)
# 	tagline = db.Column(db.String(300), nullable=True)
# 	runtime = db.Column(db.String(10), nullable=True)
# 	budget = db.Column(db.String(300), nullable=True)
 
    

# 	def __repr__(self):
# 		return '<Movie %r>' % self.title

# db.create_all()


API_KEY = "aaa5b990b039682b1209b8c632abb25e"
URL = "https://www.bfi.org.uk/sight-and-sound/greatest-films-all-time"
SEARCH_API_ENDPOINT = 'https://api.themoviedb.org/3/search/movie'
MOVIE_ENDPOINT = 'https://api.themoviedb.org/3/movie/'
r = requests.get(url=URL)
soup = BeautifulSoup(r.text, 'html.parser')




####### TESTING #################
# title = soup.find("h2", {"class": 'Headline__H2-sc-uipteu-2'})


# r = requests.get(url=title.a.get('href'))
# soup = BeautifulSoup(r.text, 'html.parser')
# year = int(soup.find("span", {"class": 'full-title-work-year'}).text[1:5])

# print(title.a.text)


# # Uses The Movie Database to get each film's details
# response = requests.get(f"{SEARCH_API_ENDPOINT}?api_key={API_KEY}&query={title.a.text}").json()['results'][0]

# movie_r = requests.get(f"{MOVIE_ENDPOINT}{response['id']}?api_key={API_KEY}").json()
# # print(movie_r["production_countries"][0]['iso_3166_1'])

# crew_r = requests.get(f"{MOVIE_ENDPOINT}{response['id']}/credits?api_key={API_KEY}").json()

# director = crew_r["crew"]
# director = next((item for item in director if item['job'] == 'Director'), None)

# # print(movie_r['overview'])

# amount = movie_r["budget"]
# currency = "{:,.0f}".format(amount)

# movie_dict = {
# 				"title": title.a.text,
# 				"director": director['name'],
# 				"country": movie_r['production_countries'][0]['name'],
# 				"year": movie_r['release_date'][0:4],
# 				"synopsis": movie_r['overview'],
# 				"img_url": f"https://image.tmdb.org/t/p/original/{movie_r['poster_path']}",
# 				"movie_url": title.a.get('href'),
# 				"tagline": movie_r['tagline'],
# 				"runtime": f"{movie_r['runtime']}mins",
# 				"budget": int(currency)
# 			}

# print(movie_dict)







####### PROGRAM ##########################

movie_db = "movie_db.json"

# Renders movie_db data in index.html
@app.route("/")
def home():
	movie_list = []
	with open(movie_db, "r") as file:
		data = json.load(file)
  
	for movie in data:
		movie_list.append(movie["title"]) 
    
	return render_template("index.html", movie_list=data)


# Retreives all the movies and movie data and stores it in movie_db.json
@app.route("/get")
def get():
	movie_list = []
	num = 1
	
 	# Finds the title of each movie from the Sight & Sound webpage  
	h2_titles = soup.find_all("h2", {"class": 'Headline__H2-sc-uipteu-2'})

	for title in h2_titles:
		try:
			r = requests.get(url=title.a.get('href'))
			soup2 = BeautifulSoup(r.text, 'html.parser')
			year = int(soup2.find("span", {"class": 'full-title-work-year'}).text[1:5])


			# Retrieves the data for the movie by getting it's title and ID for The Movie Database API
			response = requests.get(f"{SEARCH_API_ENDPOINT}?api_key={API_KEY}&query={title.a.text}&year={year}").json()['results'][0]
			movie_r = requests.get(f"{MOVIE_ENDPOINT}{response['id']}?api_key={API_KEY}").json()
			crew_r = requests.get(f"{MOVIE_ENDPOINT}{response['id']}/credits?api_key={API_KEY}").json()
   
			director = crew_r["crew"]
			director = next((item for item in director if item['job'] == 'Director'), None)

			amount = movie_r["budget"]
			if int(amount) != 0:
				currency = "${:,.0f}".format(amount)
			else:
				currency = 0
   
			
   
   
			# Retreived data stored in dictionary and appended to list of dictionaries.
			movie_dict = {
				"num": num,
				"title": title.a.text,
				"director": director['name'],
				"country": movie_r['production_countries'][0]['name'],
				"year": str(year),
				"synopsis": movie_r['overview'],
				"img_url": f"https://image.tmdb.org/t/p/original/{movie_r['poster_path']}",
				"movie_url": title.a.get('href'),
				"tagline": movie_r['tagline'],
				"runtime": f"{movie_r['runtime']}mins",
				"budget": currency
			}
			print(movie_dict["title"])
			movie_list.append(movie_dict)
			num += 1
   
		except:
			pass

	# Completed list of movie dictionaries written to movie_db.json
	with open(movie_db, "w") as file:
		json.dump(movie_list, file, indent=4, separators=(',', ': '))
    
	return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)









