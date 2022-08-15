from bs4 import BeautifulSoup
import requests
import re
from os.path  import basename

i = 1
movie_names = []
movie_links = []

#Go and get them.
while i < 124:
     i += 1

     #page_link
     page_link = "/page/"+str(i)
     html_doc = requests.get("https://web.archive.org/web/20161119235351/http://www.politikfilm.org"+page_link)
                             
     soup = BeautifulSoup(html_doc.text, 'html.parser')
     h4_titles  = soup.find_all("h4",{"class":"short-link"})
     print(str(i)+"------------------------------------------------------------")
     print(h4_titles)
     print(str(i)+"------------------------------------------------------------")
    
     for title in h4_titles:

         #print(a.text)
         movie_names.append(title.text)

         #Movie link
         a = title.find("a")
         movie_links.append(a["href"])

#Get movie details
def get_movie_detail(movie_links):
    mo = 0
    for link in movie_links:
        mo +=1
        #Make one more query to getting details
        try:
            html_doc = requests.get(link)
            detail_page = BeautifulSoup(html_doc.text, 'html.parser')

            print(str(mo)+"##################################################")
            print(detail_page)
            print(str(mo)+"##################################################")

            movie_poster    = detail_page.find("div",{"class":"fstory-poster"}).find("img")["src"]
            movie_name      = detail_page.find("h1",{"class":"fstory-h1"}).text
            movie_cover     = detail_page.find("div",{"class":"fstory-content margin-b40 block-p"}).text
            movie_director  = detail_page.find_all("div",{"class":"finfo"})[1].find("div",{"class":"finfo-text"}).text
            movie_year      = detail_page.find_all("div",{"class":"finfo"})[2].find("div",{"class":"finfo-text"}).text
            movie_type      = detail_page.find_all("div",{"class":"finfo"})[4].find("div",{"class":"finfo-text"}).text
            movie_actors      = detail_page.find_all("div",{"class":"finfo"})[6].find("div",{"class":"finfo-text"}).text

            #To get poster
            prefix_match = re.findall(r"""https://""", movie_poster)
            if not prefix_match:
                movie_poster = "https://web.archive.org/"+movie_poster
            
            #download the image
            with open("./site/poster/"+basename(movie_poster),"wb") as f:
                f.write(requests.get(movie_poster).content)

            movie_template = ""           
            movie_template += '\n<div id="movie">\n' 
            movie_template += '<h1 class="movie-name">'+str(mo)+' |  '+movie_name+'</h1>\n'
            movie_template += '<p class="movie-director">'+movie_director+' | '+movie_type+' | '+movie_year+'</p>\n'
            movie_template += '<p class="movie-actors">'+movie_actors+'</p>\n'
            movie_template += '<img src="'+"./poster/"+basename(movie_poster)+'">\n'
            movie_template += '<p class="movei-cover">'+movie_cover+'</p>\n'
            movie_template += '</div>\n'

            # append the new movie to the html file.
            with open("./site/index.html", "a") as index_file:
                index_file.write(movie_template) 
            
        except:
            continue

#Names#1: Save all names to file
def save_to_file(datas, file_name = "./site/politikfilm.org.txt",link=False):

    with open(file_name, "w") as file:
        j = 0
        for data in datas:
            j +=1
            if not link:
                file.write(str(j)+" - "+data+"\n")
            else:
                file.write(data+"\n")

get_movie_detail(movie_links)

save_to_file(movie_names)
#save_to_file(movie_links,"./site/politikfilm_links.txt", True)