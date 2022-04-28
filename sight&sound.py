from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)


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









