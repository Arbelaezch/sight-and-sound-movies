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

# title = soup.find("h2", {"class": 'Headline__H2-sc-uipteu-2'})

# # Uses The Movie Database to get each film's details
# response = requests.get(f"{SEARCH_API_ENDPOINT}?api_key={API_KEY}&query={title.a.text}").json()['results'][0]
# movie_r = requests.get(f"{MOVIE_ENDPOINT}{response['id']}?api_key={API_KEY}").json()
# crew_r = requests.get(f"{MOVIE_ENDPOINT}{response['id']}/credits?api_key={API_KEY}").json()

# director = crew_r["crew"]
# director = next((item for item in director if item['job'] == 'Director'), None)


# print(director['name'])

#################################
# print(title.a.get('href'))



@app.route("/")
def home():
    
    
	return render_template("index.html", movie_list=movie_list)


@app.route("/get")
def get():
	movie_list = []
	# Finds the title of each movie from the Sight & Sound webpage  
	h2_titles = soup.find_all("h2", {"class": 'Headline__H2-sc-uipteu-2'})

	for title in h2_titles:
		try:
			response = requests.get(f"{SEARCH_API_ENDPOINT}?api_key={API_KEY}&query={title.a.text}").json()['results'][0]
			movie_r = requests.get(f"{MOVIE_ENDPOINT}{response['id']}?api_key={API_KEY}").json()
			crew_r = requests.get(f"{MOVIE_ENDPOINT}{response['id']}/credits?api_key={API_KEY}").json()
   
			director = crew_r["crew"]
			director = next((item for item in director if item['job'] == 'Director'), None)
			# print(director['name'])
   
			movie_dict = {
				"title": title,
				"director": director['name'],
				"country": movie_r['production_countries']['iso_3166_1'],
				"year": movie_r['release_date'][0:4],
				"synopsis": movie_r['Overview'],
				"img_url": f"https://image.tmdb.org/t/p/original/{movie_r['poster_path']}",
				"movie_url": title.a.get('href'),
				"tagline": movie_r['tagline'],
				"runtime": movie_r["runtime"],
				"budget": movie_r["budget"]
			}
   
			movie_list.append(movie_dict)


			# For if I want to use an SQL db instead of JSON.
			# movie = Movie(id=response["id"], title=title, director=movie_r[''], country=movie_r[''], year=movie_r['release_date'][0:4], synopsis=movie_r[''], img_url=movie_r[''], movie_url=title.a.get('href'), tagline=movie_r[''], runtime=movie_r[''], budget=movie_r[''])
   
		except:
			pass
    
	return redirect("index.html")



if __name__ == "__main__":
    app.run(debug=True)









