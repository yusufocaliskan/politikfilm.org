from bs4 import BeautifulSoup
import json

html_doc=  open("index.html","r")

soup = BeautifulSoup(html_doc, 'html.parser')
all_movie_raw = soup.find_all("div",{"class":"movie"})

movie_container = []
i = 0
for movie in all_movie_raw:
    i += 1
    title = movie.find("h1").text.strip()
    info = movie.find("p",{"class":"movie-director"}).text.split("|")
    director = info[0]
    category = info[1]
    year = info[2]
    actors = movie.find("p",{"class":"movie-actors"}).text.split(",")
    poster = movie.find("div",{"class":"movie-poster"}).find("img")["src"].split("/")[2]
    summary = movie.find("p",{"class":"movei-cover"}).text.strip()

    movie_container += [{
        "title":title,
        "director":director,
        "category":category,
        "year":year,
        "actors":actors,
        "poster":poster,
        "summary":summary
        }]    


#Save it
with open("data.json","w", encoding="utf-8") as data:
    json.dump(movie_container, data, ensure_ascii= False, indent=4)