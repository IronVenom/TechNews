from flask import Flask , redirect , url_for , render_template
import requests
import feedparser
from newsapi import NewsApiClient

app = Flask(__name__)
newsapi = NewsApiClient(api_key=API_KEY)

@app.route("/")
def home_page():
	return render_template("index.html")

@app.route("/nasa-apod")
def nasa_apod():

	info = requests.get('https://api.nasa.gov/planetary/apod?api_key=API_KEY').text
	information = eval(info)['explanation']
	title = eval(info)['title']
	url = None

	try:
		url = eval(info)['hdurl']
	except KeyError:
		url = eval(info)['url']

	image_check = ['jpg','png','jpeg']

	videocheck = "True"

	for i in image_check:
	    if i in url:
	        videocheck = "False"

	if 'https:' in url:
		return render_template("apod.html",url = url,information = information,title = title,videocheck = videocheck)
	else:
		url = 'https:'+url
		return render_template("apod.html",url = url,information = information,title = title,videocheck = videocheck)

@app.route("/articles")
def articles():

	sec_news = feedparser.parse('https://techxplore.com/rss-feed/security-news/')
	titles = [i['title'] for i in sec_news['entries']]
	summary = [i['summary'] for i in sec_news['entries']]
	link = [i['link'] for i in sec_news['entries']]
	pics = []
	for i in sec_news['entries']:
		try:
			pics.append(i['media_thumbnail'][0]['url'])
		except:
			pics.append(False)
	securityNews = ["Cyber Security",titles,summary,link,pics]

	ml_news = feedparser.parse('https://techxplore.com/rss-feed/machine-learning-ai-news/')
	titles = [i['title'] for i in ml_news['entries']]
	summary = [i['summary'] for i in ml_news['entries']]
	link = [i['link'] for i in ml_news['entries']]
	pics = []
	for i in ml_news['entries']:
		try:
			pics.append(i['media_thumbnail'][0]['url'])
		except:
			pics.append(False)
	mlNews = ["Machine Learning",titles,summary,link,pics]

	software_news = feedparser.parse('https://techxplore.com/rss-feed/software-news/')
	titles = [i['title'] for i in software_news['entries']]
	summary = [i['summary'] for i in software_news['entries']]
	link = [i['link'] for i in software_news['entries']]
	pics = []
	for i in software_news['entries']:
		try:
			pics.append(i['media_thumbnail'][0]['url'])
		except:
			pics.append(False)
	softwareNews = ["Software",titles,summary,link,pics]

	cs_news = feedparser.parse('https://techxplore.com/rss-feed/computer-sciences-news/')
	titles = [i['title'] for i in cs_news['entries']]
	summary = [i['summary'] for i in cs_news['entries']]
	link = [i['link'] for i in cs_news['entries']]
	pics = []
	for i in cs_news['entries']:
		try:
			pics.append(i['media_thumbnail'][0]['url'])
		except:
			pics.append(False)
	csNews = ["Computer Science",titles,summary,link,pics]

	return render_template("articles.html",securityNews = securityNews, mlNews = mlNews , softwareNews = softwareNews , csNews = csNews)
	
@app.route("/news")
def news():
	
	engadget=newsapi.get_everything(q='technology',sources='engadget',language='en')['articles']
	techcrunch=newsapi.get_everything(q='technology',sources='techcrunch',language='en')['articles']
	techradar=newsapi.get_everything(q='technology',sources='techradar',language='en')['articles']
	
	return render_template("news.html",techcrunch=techcrunch,techradar=techradar,engadget=engadget)
if __name__ == "__main__":
    app.run(debug=True)
