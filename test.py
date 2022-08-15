import wikipedia
wikipedia.set_lang("en")
movie = wikipedia.page("daisy Diamond (2007)")

print(movie.links)