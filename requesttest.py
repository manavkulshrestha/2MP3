import pprint
from urllib import request

# pp = pprint.PrettyPrinter(indent=2)

# page = request.urlopen('https://play.google.com/music/preview/pl/AMaBXylTOd8jts6Whb1G-ty-EiYLuqy5uqcoPrH9a1bIQm9ukeaKpoxN35KkQfwJMKcJXNiv3Fjl413JcDgKred0uHzmHKUyFQ==?u=0')

# pp.pprint(page.read())

from bs4 import BeautifulSoup
html = request.urlopen('https://play.google.com/music/preview/pl/AMaBXylTOd8jts6Whb1G-ty-EiYLuqy5uqcoPrH9a1bIQm9ukeaKpoxN35KkQfwJMKcJXNiv3Fjl413JcDgKred0uHzmHKUyFQ==?u=0').read()
parsed_html = BeautifulSoup(html)
print(parsed_html.prettify())
print(parsed_html.body.find('div', attrs={'class':'content-container'}))