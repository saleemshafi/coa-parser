import requests
import re
from bs4 import BeautifulSoup
import os

def downloadFile(baseDir, url):
	r = requests.get(url)

	cdrh = r.headers['content-disposition']
	if cdrh != None:
		for c in cdrh.split(';'):
			if c.find("filename=") == 0:
				filename = c[9:]
	else:
		filename = url[url.rfind('/')+1:]
		if "?" in filename:
			filename = filename[:filename.find('?')]

	print("Saving "+url+" as "+filename)
	with open(baseDir+"/"+filename, 'wb') as f:
	    f.write(r.content) 


def getMinuteUrls(url):
	print("Visiting "+url)
	html = os.popen('curl -s '+url).read()

	soup = BeautifulSoup(html, 'html.parser')
	mainSection = soup.find(id="bcic")
	for link in mainSection.find_all('a'):
		path = link.get('href')
		for text in link.stripped_strings:
			if "Minutes" in text:
				yield path


urls = []
with open('./urls.txt','rt') as f:
	for line in f:
		urls.append(line)

for url in urls:
	for minutesUrl in getMinuteUrls(url):
		downloadFile('./minutes',minutesUrl)
