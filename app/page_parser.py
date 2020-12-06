import requests
import re
from bs4 import BeautifulSoup

def scrapeHTML(URL):

	url = URL
	res = requests.get(url)
	html_page = res.content
	soup = BeautifulSoup(html_page, 'html.parser')
	text = soup.find_all(text=True)

	output = ''
	blacklist = [
		'[document]',
		'noscript',
		'header',
		'html',
		'meta',
		'head', 
		'input',
		'script',
	
		# there may be more elements you don't want, such as "style", etc.
	]

	for t in text:
		if t.parent.name not in blacklist:
			output += '{} '.format(t)

	
	output = re.sub(r'  +', ' ', output)
	output = re.sub(r'\s\s\s+', '\n\n', output)

	return output