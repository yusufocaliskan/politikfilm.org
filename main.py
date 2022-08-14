from bs4 import BeautifulSoup
import requests

i = 0
movie_names = []
while i < 127:
    i += 1
    html_doc = requests.get("https://web.archive.org/web/20161210110041/http://politikfilm.org/page/"+str(i))
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    h4  = soup.find_all("h4",{"class":"short-link"})
    for a in h4:
        #print(a.text)
        movie_names.append(a.text)

with open("politikfilm.org.txt", "w") as file:
    j = 0
    for movie in movie_names:
        j +=1
        file.write(str(j)+" - "+movie+"\n")