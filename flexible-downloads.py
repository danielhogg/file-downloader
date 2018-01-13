import os
import sys

import requests
from bs4 import BeautifulSoup

import wget
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://inst.eecs.berkeley.edu/~cs170/fa17/'
page = requests.get(url + 'calendar.html')
soup = BeautifulSoup(page.text, 'html.parser')

weekly_rows = soup.find_all('tbody')
weekly_links = []

for wk in weekly_rows: 
	lnks = wk.find_all('a')
	if lnks:
		weekly_links.append(lnks)

urls = []
keyword = 'assets'

# keeps lnk if it starts with assets
def extract_link(lnk):
	href = lnk['href']
	if href[0:6] == keyword:
		return url + '/' + href

for lnks in weekly_links:
	extracted_with_none = list(map(extract_link, lnks))
	extracted_without_none = list(filter(lambda x: x is not None, extracted_with_none))
	urls.extend(extracted_without_none)

path = '/Users/Annie/file-downloader/test-folder'
prompt = "Do you want to download {}?\n\
Enter [Y]es/[N]o/[Q]uit here: "

def verify(ans):
	return ans == 'y' or ans == 'yes'
def quit(ans):
	return ans == 'q' or ans == 'quit'



for url in urls:
	r = requests.get(url)
	if r.status_code != 404:
		filename = os.path.basename(url) 
		answer = input(prompt.format(filename))
		if verify(answer.lower()):
			wget.download(url, out=path)
			print()
		elif quit(answer.lower()):
			break
