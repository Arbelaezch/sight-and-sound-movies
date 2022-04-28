from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/sight-and-sound.db'
db = SQLAlchemy(app)

class Movie(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
	director = db.Column(db.String(50), nullable=False)
	country = db.Column(db.String(20))
	year = db.Column(db.String(4), nullable=False)
	synopsis = db.Column(db.String(300))
    

	def __repr__(self):
		return '<Movie %r>' % self.title





URL = "https://www.bfi.org.uk/sight-and-sound/greatest-films-all-time"

r = requests.get(url=URL)
soup = BeautifulSoup(r.text, 'html.parser')


@app.route("/")
def home():
	movie_list = []
    
	h2 = soup.find_all("h2", {"class": 'Headline__H2-sc-uipteu-2'})

	num = 1

	for movie in h2:
		try:
			movie = f"{movie.a.text}"
			movie_list.append(movie)
			num += 1
		except:
			pass
    
	return render_template("index.html", movie_list=movie_list)



if __name__ == "__main__":
    app.run(debug=True)









