#Service.py
import time
import spotipy
import spotipy.util as util
from youtube_search import YoutubeSearch
from pprint import pprint as pp
from google_trans_new import google_translator

from bs4 import BeautifulSoup
import requests
import lxml, urllib

from threading import Thread

import os, requests, uuid, json, re
import requests
from youtube_title_parse import get_artist_title
from google_trans_new import google_translator
from bs4 import BeautifulSoup, UnicodeDammit, NavigableString
translator = google_translator()

from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from googlesearch import search

translator = google_translator()

import traceback



class MusicService(object):
	id = "Music"
	name = "🔊 Music 🔊"
	welcome = "*Welcome to Music 🔊 Service!* \n\nSend us the name of a song to get *Youtube* and *Spotify* Links :)"+"\n*שלחו שם של שיר :)*"
	help = "send a message to get it back"
	imageurl = "https://i.imgur.com/lpjQPk5.jpg"
	shortDescription = "Just get your music"
	share = None

	examples = {"example1":{"text":"","thumbnail":None, "answer":"sweet child"}, "example2":{"text":"","thumbnail":None, "answer":"כחולת עינים"}}
	coms = ["Scraper"]

	def __init__(self,db, api):
		MusicService.share = self

		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! MusicService",MusicService.share)
		self.db = db
		self.api = api
		if "upcoming" not in self.db:
			self.db["upcoming"] = []
		if "users" not in self.db:
			self.db["users"] = {}

		self.spotify = None
		self.spotiAlive()

	''' restarts spotify to keep it alive '''
	def spotiAliveAsync(self, data):
		while(True):
			try:
				token = spotipy.SpotifyClientCredentials(client_id ='d419f4fe1de143c0ab7561734322fbe2', client_secret='a5738d2f12a44336b74153cc96a1946e')
				cache_token = token.get_access_token()
				self.spotify = spotipy.Spotify(cache_token)
			except Exception as e:
				print()
				print("EEEEEEEEEEEEEE spotify init",e)
				print("EEEEEEEEEEEEEE spotify init",e)
				print("EEEEEEEEEEEEEE spotify init",e)
				print()
				print()
				traceback.print_exc()
			time.sleep(30*60)


	def spotiAlive(self):
		st = Thread(target = self.spotiAliveAsync, args = [None])
		st.start()

	def go(self):
		while(False):
			if "upcoming" not in self.db:
				self.db["upcoming"] = []
			if "users" not in self.db:
				self.db["users"] = {}

			while len(self.db["upcoming"]) > 0:
				item = self.db["upcoming"].pop(0)
				origin, content = item
				self.api.send(origin, content)
				# self.api.backup(self.db)

			time.sleep(1)


	def artistInHebrew(self,q, s = 20, lang = None):
		# return search(q,stop = s)
		text = urllib.parse.quote_plus(q+" hebrew")
		url = 'https://google.com/search?q=' + text
		if lang is not None:
			url = url.replace(".com",lang)
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'lxml')
		res = soup.text
		if "hebrew:" in res.lower():
			artistHeb = " ".join(res.lower().split("hebrew: ")[1].split(" ")[:len(q.split(" "))])
			while not artistHeb[-1].isalpha():
				artistHeb = artistHeb[:-1]
			return artistHeb
		return q



	def downloadImage(self,songURL= 'https://www.tab4u.com/tabs/songs/68069_יסמין_מועלם_-_מסיבה.html'):
		driver = webdriver.Chrome()
		url = 'https://web-capture.net/'
		driver.get(url)
		l = driver.find_element_by_id("link")
		l.send_keys(Keys.SHIFT+Keys.HOME)
		l.send_keys(Keys.BACKSPACE)
		l.send_keys(songURL+Keys.ENTER)
		go = "https://web-capture.net/picture.php?pic_index=1&presentation_method=inline"
		driver.get(go)
		i = driver.find_element_by_tag_name("img")



# l = driver.find_element_by_id("link")
# l.send_keys(songURL+Keys.ENTER)

	def urlCheck(self, query):
		print("QQQQQQQQQQQQQQQQ",query)
		if query is "":
			return  render_template('base.html',title = u"\U0001F49A")
		urlChecks = ["http","youtu","spotify"]
		url = False
		for check in urlChecks:
			if check.lower() in query.lower():
				url = True
		print("START")
		processed_text = ""
		if url:
			print(query,"!!!!!!!!!!!!!!!!!!!")
			query = str(re.search("(?P<url>https?://[^\s]+)", query).group("url"))
			print(query,"!!!!!!!!!!!!!!!!!!!!")
			html = self.getHTML(query)
			try:
				if "spotify" in query:
					full = html.title.string
					full = full.split(', a song by ')
					full[1] = full[1].split(" ")[0].replace(","," ")
					title, artist = full
					title = str(re.sub(r" ?\([^)]+\)", "", title))
					artist = str(re.sub(r" ?\([^)]+\)", "", artist))
					processed_text = title +" "+artist
					print(processed_text)
				else:
					processed_text = "-".join(html.title.string.split("-")[:-1]).replace("/"," ")
			except Exception as e:
				print("EEEEEEEEEEEEEEEEEE: Processing Text ",e)
				processed_text = ""
				return query, None, None
				# return render_template('base.html')
			print("UUUUUUUUUUUUUUUUUUUUUU",processed_text)
			print("UUUUUUUUUUUUUUUUUUUUUU",processed_text)
			print("UUUUUUUUUUUUUUUUUUUUUU",processed_text)
		else:
			processed_text = query
		if processed_text == "":
			return " ", None, None
		return processed_text, None, None


	def getHTML(self, url):
		headers_Get = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				'Accept-Language': 'en-US,en;q=0.5',
				'Accept-Encoding': 'gzip, deflate',
				'DNT': '1',
				'Connection': 'keep-alive',
				'Upgrade-Insecure-Requests': '1'
			}
		searchPage = requests.get(url, headers=headers_Get)
		html = BeautifulSoup(searchPage.text,'html.parser')
		return html

	def getLyrics(self, title):
		# return lyricwikia.get_lyrics('Led Zeppelin', 'Stairway to heaven')
		# search("")
		# print("title",title)
		url='https://www.google.com/search?q='
		# s=input('Enter the song to find its lyrics: ')
		s = '\"'+title+'\"'
		#calculating time taken in searching lyrics
		# a = datetime.datetime.now()
		for i in s:
			if i==' ':
				url+='+'
			else:
				url+=i
		url+='+lyrics'
		html = self.getHTML(url)
		# print("\n#####",html,"\n###########")
		song_info = []
		song_title = []
		for paper in html.findAll("div",class_="auw0zb"):
			for desc in paper.descendants:
				print("DDDDDDDD",desc)
			info = [desc.strip() for desc in paper.descendants if type(desc) == NavigableString]
			for i in info:
				song_title.append(i)
		print("\n#####333333",song_title,"\n###########")
		if len(song_title) > 1:
			songtitle = song_title[1].split(" lyrics ©")[0]
			song_info.append(songtitle)
		artists = []
		for paper in html.findAll("div",class_="wx62f PZPZlf x7XAkb"):
			for desc in paper.descendants:
				print("DDDDDDDD",desc)
			info = [desc.strip() for desc in paper.descendants if type(desc) == NavigableString]
			for i in info:
				artists.append(i)
		print("\n#####",artists,"\n###########")
		if len(artists) > 0:
			artist = artists[0].replace("Song by ","")
			song_info.append(artist)
		if len(song_info) < 2:
			print("wwwwwwwwwwww",song_info)
			song_info = []
			for paper in html.findAll("div",class_="SPZz6b"):
				for desc in paper.descendants:
					print("DDDDDDDD",desc)
				info = [desc.strip() for desc in paper.descendants if type(desc) == NavigableString]
				for i in info:
					song_info.append(i)
		lyrics=html.find_all("span", jsname="YS01Ge")
		if lyrics==[]:
			print('Couldn\'t get lyrics')
		else:
			nlyr = ""
			nl = ["; ","\n"]
			c = 0
			for i in lyrics:
				# print(i.get_text())
					nlyr += i.get_text() + nl[c%2]
					c+=1
			return nlyr, song_info


	def chunks(self, lst, n):
	    """Yield successive n-sized chunks from lst."""
	    for i in range(0, len(lst), n):
	        yield lst[i:i + n]

	def danilator(self, item, withTranslations = False, lang_tgt="he", lyrics = None):
		if item == "":
			return "", ["",""]
			# item = input('Enter the song to find its lyricsxx: ')
		res = None
		maxTries = 4
		mc = 0
		song_info = None
		if lyrics is None:
			lyricsText, song_info = "sorry, lyrics not found, try again soon ",["Could not find lyrics",item]
			while res is None and mc <= maxTries:
				# try:
				target = item
				print("ITEM:"+target)
				artist_title = get_artist_title(target)
				if artist_title is not None:
					print("@@@@@@@@@@@@@@@@@@@@",artist_title)
					artist, title = artist_title
					if mc==1:
						target = title+" " + artist
						item = item.replace("&"," and ")
					if mc==2:
						target = title+" " + artist.split(" ")[0]
					if mc==3:
						target = title
				else:
					print("!!!!!!!!!!!!!!!!!!!!!!!!")
					print("!!!!!!!!!!!!!!!!!!!!!!!!")
					print("!!!!!!!!!!!!!!!!!!!!!!!!")
				print("TTTTTTTTTTTTTTTTT")
				print(target)
				print("TTTTTTTTTTTTTTTTT")
				# except:
				# 	print("E: could not parse artist and title")
				res = self.getLyrics(target)
				mc+=1
				if res is not None and len(res) > 1:
					lyricsText, song_info = res
			chars = [["-"," "],["(",""],[")",""],["~",""],["\r",""]]
			for c in chars:
				lyricsText = lyricsText.replace(c[0],c[1])
			# .replace().replace("(","").replace(")","")
			lyrics = []
			for l in lyricsText.split("\n"):
				lyrics.append(l)
			# body = [{
		# 	'text' : lyricsText
		# }]
		else:
			lyricsText = "\n".join(lyrics).replace("\r","")

		translated = []
		if withTranslations:
			n = 0
			parts = []
			print(lyricsText)
			print(type(lyricsText), len(lyricsText),len(lyricsText.split("\n")))
			maxChunks = 50
			for chunk in self.chunks(lyricsText.split("\n"), maxChunks):
				chunkT = "~".join(chunk)
				print("!!!!!!!!!!!!","\n",chunkT)
				res = translator.translate(str(chunkT),lang_tgt = lang_tgt)
				print("$$$$$$$$$$$$$$$$$$$$$")
				print(res)
				parts.append(res+"\n")
			# time.sleep(1)
				# n+=1
			# res = translator.translate(lyricsText,lang_tgt="he")
			print("########################@@@")
			print(parts)
			# translated = res.__dict__()["text"]
			translated = ("\n".join(("".join(parts)).split("~"))).split("\n")
			print("############################")
			print(translated)
			print("XXXXXXXXXXXXXXXXXXXXXXXXXXX")
		fullL = []
		# fullt = "<h1>"+item+"</h1>"
		for c in range(len(lyrics)):
			fullL.append(lyrics[c])
			if c < len(translated):
				fullL.append(translated[c])
				fullL.append("")
				# fullL.append("")
			# fullt += "<pre>"+lyrics[c] + "</pre>"
			# fullt += "<pre>"+translated[c][::-1] + "</pre>"
			# print(lyrics[c])
			# print(translated[c])
			print("")
		print(" @ @ @ @ @ @  @")
		print(fullL)
		return "\n".join(fullL), song_info

	def process(self, info):
		origin, user, content = None, None, None
		if "origin" in info:
			origin = info["origin"]
		if "user" in info:
			user = info["user"]
		if "content" in info:
			content = info["content"]

		if "users" not in self.db:
			self.db["users"] = {}

		if origin not in self.db["users"]:
			self.db["users"][origin] = {"history":{}}

		hasCMD = False
		sent = False
		if origin.split("/")[0] in self.coms:
			hasCMD = True
			lastOrigin = "/".join(origin.split("/")[1:])
			add = ""
			if len(lastOrigin.split("/")) > 1:
				id = lastOrigin.split("/")[1]
				history = self.db["users"][lastOrigin.split("/")[0]]["history"]
				if len(history) >= int(id)+1:
					song = history[id]
					if song is not None:
						add = song["search"]
						if "title" in song:
							add = song["title"]
						if "artist" in song:
							add += " " + song["artist"]
						add +":\n"
				if "danilator" in origin:
					print("@@@@@@@@@@@@@@@")
					print("@@@@@@@@@@@@@@@")
					print("@@@@@@@@@@@@@@@")
					print("@@@@@@@@@@@@@@@")
					print("@@@@@@@@@@@@@@@")
					print("@@@@@@@@@@@@@@@",content)
					targetLanguage = "en"
					target = origin.split("danilator")[1]
					if len(target.split("/")) > 1:
						targetLanguage = target.split("/")[1]

					nlyr = ""
					nl = ["; ","\n"]
					c = 0
					for i in content.split("\n"):
						# print(i.get_text())
							nlyr += i + nl[c%2]
							c+=1

					lyrics = []
					for l in nlyr.split("\n"):
						if len(l) > 0:
							print("@@@:"+l)
							lyrics.append(l)
					# lyrics = content
					content, _ = self.danilator(song["search"],withTranslations=True,lang_tgt=targetLanguage,lyrics=lyrics)

					# cleanlyrics = []
					# for l in content.split("\n"):
					# 	if len(l) > 0:
					# 		print("@@@:"+l)
					# 		cleanlyrics.append(l)
					# content = "\n".join(cleanlyrics)
					print("###########")
					print("###########")
					print("###########")
					print("###########")
					print("###########",content)
					sent = True
					self.api.send(lastOrigin.split("/")[0], add+"\n"+content)

			if not sent:
				self.api.send(lastOrigin.split("/")[0], add+"\n"+content)
		else:

			if origin not in self.db["users"] or "history" not in self.db["users"][origin]:
				self.db["users"][origin] = {"history":{}}

			history = self.db["users"][origin]["history"]

			# self.api.send(origin, "ECHO |"+content+"|")

		print("::::::::::::::::::::::::::::::::::::::::::::::::::::::")
		print("::::::::::::::::::::::::::::::::::::::::::::::::::::::")
		print("::::::::::::::::::::::::::::::::::::::::::::::::::::::")
		print("::::::::::::::::::::::::::::::::::::::::::::::::::::::")
		print("::::::::::::::::::::::::::::::::::::::::::::::::::::::")
		print("::::::::::::::::::::::::::::::::::::::::::::::::::::::")
		print("::::::::::::::::::::::::::::::::::::::::::::::::::::::")
		print("::::::::::::::::::::::::::::::::::::::::::::::::::::::")
		print("::::::::::::::::::::::::::::::::::::::::::::::::::::::")
		print("::::::::::::::::::::::::::::::::::::::::::::::::::::::")
		print("::::::::::::::::::::::::::::::::::::::::::::::::::::::")
		print("::::::::::::::::::::::::::::::::::::::::::::::::::::::")
		print(content)
		print()
		print()
		if ":" == content[0]:
			if len(content.split(":")) > 2 and len(content.split(":")[2])>0:

				hasCMD = True
				l = content.split(":")
				id = l[1]
				try:
					cmd = l[2]
					print("CMD",cmd,"id",id,"HIST",history)
					if len(history) >= int(id)+1:
						song = history[id]
						title = ""
						artist = ""
						if song is not None:
							if "title" in song:
								title = song["title"]
							if "artist" in song:
								artist = song["artist"]

						if title is "":
							title = song["search"]

						if cmd == "more":
							sendLinks = ""
							link = song["link"]

							sendLinks += "Looking for other Artist?:\n"+link+":other"+"\n\n"
							sendLinks += "Get Song Lyrics:\n"+link+":lyrics"+"\n"
							sendLinks += "Lyrics Translation:\n"+link+":danilator"+"\n"
							sendLinks += "Get Chords:\n"+link+":chords"+"\n"
							#
							# answer = ":lyrics:"+str(songID)
							# link = self.api.genLink(origin, answer, newLink = str(songID)+"-lyrics")
							#
							# answer = ":danilator:"+str(songID)
							# link = self.api.genLink(origin, answer, newLink = str(songID)+"-danilator")
							# sendLinks += "Lyric Translation: "+link+"\n"
							#
							# answer = ":chords:"+str(songID)
							# link = self.api.genLink(origin, answer, newLink = str(songID)+"-chords")
							# sendLinks += "Get Chords: "+link+"\n"
							# time.sleep(1.5)
							self.api.send(origin, sendLinks, thumnail = None)
						if cmd == "other":
							self.api.send(origin, "FINDING OTHER ARTIST FOR "+title+" "+artist)
							newArtists = []
							if "artist" in song:
								results = self.spotify.search(song["search"])
								if len(results) > 0 and "tracks" in results and "items" in results["tracks"]:
									for res in results['tracks']['items']:
										# link = res['external_urls']['spotify']
										# title = res["name"]
										newArtist = res["album"]["artists"][0]["name"]
										if song["artist"].lower() == newArtist.lower():
											pass
										else:
											newArtists.append(res["name"]+" "+newArtist)
										# image = res["album"]["images"][1]['url']
							title = song["search"]
							sendArtist = ""

							for nA in newArtists:

								link = "link"+" "+nA
								sendArtist +=  "*"+nA+"* : \n"+ link+"\n"

							self.api.send(origin, "More Artist:\n"+sendArtist)

						if cmd == "lyrics":
							print("LLLLLLLLLLLLLLLLLLLLLLLLLLL")
							print("LLLLLLLLLLLLLLLLLLLLLLLLLLL")
							print("LLLLLLLLLLLLLLLLLLLLLLLLLLL")
							print("LLLLLLLLLLLLLLLLLLLLLLLLLLL")

							if song["language"] is "hebrew":
								# try:
								if "artist" in song and translator.detect(song["artist"])[1] is not "hebrew":
									artist = self.artistInHebrew(artist)
										# artist = song["artist"] = translator.translate(song["artist"],lang_tgt="he")
								# 	if "title" in song and translator.detect(song["title"])[1] is not "hebrew":
								# 		title = song["title"] = translator.translate(song["title"],lang_tgt="he")
								# except :
								# 	traceback.print_exc()
								self.api.send(origin, "FINDING LYRICS ARTIST FOR "+title+" "+artist)
								print("LLLLLLLLLLLLLLLLLLLLLLLLLLL")
								self.api.send("Scraper"+"/"+origin+"/"+id, ":shironet:"+title+" "+artist+" shironet")
								# self.api.send("Scraper"+"/"+origin, ":shironet:"+song["search"]+" shironet")
							else:

								fullT, songInfo = self.danilator(title+" "+artist)
								header = "*"+title
								if artist is not "":
									header += " - "+artist+"*\n\n"
								else:
									header += "*\n\n"

								# print("songInfo", songInfo)
								# print("songInfo", songInfo)
								# print("songInfo", songInfo)
								# print("songInfo", songInfo)
								print("songInfo", songInfo)
								self.api.send(origin, header+fullT)
								# self.api.send("Scraper"+"/"+origin, ":googlelyrics:"+title+" "+artist+" lyrics")

						if cmd == "chords":
							self.api.send(origin, "FINDING CHORDS ARTIST FOR "+title+" "+artist)

						if cmd == "danilator":
							if song["language"] is "english":
								fullT, songInfo = self.danilator(title+" "+artist, withTranslations=True)
								header = "*"+title
								if artist is not "":
									header += " - "+artist+"*\n\n"
								else:
									header += "*\n\n"

								print("songInfo", songInfo)
								print("songInfo", songInfo)
								print("songInfo", songInfo)
								print("songInfo", songInfo)
								print("songInfo", songInfo)
								self.api.send(origin, header+fullT)
							elif song["language"] is "hebrew":
								self.api.send("Scraper"+"/"+origin+"/"+id+"/danilator/en", ":shironet:"+title+" "+artist+" shironet")


					# self.api.send(origin, "FUCK YEA "+content)
				except :
					traceback.print_exc()

		if not hasCMD:


			songID = str(len(history))
			lang = "english"

			check, uTitle, uArtist = self.urlCheck(content)
			if check != content:
				try:
					print("FROM URL",check)
					# get title artist
					res = translator.detect(check)
					if res is not None and len(res) > 1:
						lang = res[1]
				except:
					traceback.print_exc()
			else:
				try:
					res = translator.detect(content)
					if res is not None and len(res) > 1:
						lang = res[1]
				except:
					traceback.print_exc()

			link = self.api.genLink(origin, ":"+str(songID)+":", newLink = ":"+str(songID))
			history[songID] = {"search":content, "language":lang, "link":link}




			# if user not in self.db["users"]:
			# 	self.db["users"][user] = user
			# 	self.api.send(origin, "WELCOME "+user)
			# 	self.backup()

			# self.db["upcoming"].append([origin, content])

			# query = "sweet child"
			thumnail = None
			sendBack = "Sorry we could not find your song on Spotify for some reason.\n\n"
			found = False
			image = self.imageurl
			try:
				results = self.spotify.search(content)
				print("# # # # # # # # ")
				# pp(results)
				# print("# # # # # # # # ")
				if len(results) > 0:
					res = results['tracks']['items'][0]
					slink = res['external_urls']['spotify']
					title = res["name"]
					artist = res["album"]["artists"][0]["name"]
					image = res["album"]["images"][1]['url']
					year = res["album"]["release_date"].split("-")[0]
					desc = artist
					if res["type"] == "track":
						desc += " • Song"
					desc += " • "+year
					thumnail = {"imageurl":image,"title":title,"desc":desc,"link":slink}
					found = True
			except Exception as e:
				print("COULD NOT FIND SONG ON SPOTIFY", e)

			search = content
			if found:
				sendBack = "Spotify: *"+title+" - "+artist+"*\n"
				sendBack += slink+"\n\n"
				search = title+" "+artist
				history[songID]["title"] = title
				history[songID]["artist"] = artist

			linkDefault = "spotify"
			ytres = None
			try:
				ytres = YoutubeSearch(search, max_results=1).to_dict()
			except :
				traceback.print_exc()

			if ytres is not None and len(ytres) == 1:
				try:
					print("# # # # # # # # ")
					print("# # # # # # # # ")
					print("# # # # # # # # ")
					print("# # # # # # # # ")
					print("# # # # # # # # ")
					print(ytres[0])
					vidID = ytres[0]['url_suffix']
					title = ytres[0]['title']
					ylink = "https://youtu.be"+vidID
					desc = ytres[0]['channel']
					image = ytres[0]["thumbnails"][0]
					if vidID is not None and len(vidID) > 0:
						sendBack+="Youtube: *"+title+"*"+"\n"+ylink

					''' thumnail for youtube '''
					if not found or linkDefault is "youtube" or False:

						thumnail = {"imageurl":image,"title":title,"desc":desc,"link":ylink}

				except Exception as e:
					print("COULD NOT FIND SONG ON YOUTUBE", e)

			self.api.send(origin, sendBack, thumnail = thumnail)


			sendLinks = ""
			answer = str(songID)

			sendLinks += link+":more"


			#
			# sendLinks = ""
			# answer = ":other:"+str(songID)
			# link = self.api.genLink(origin, answer, newLink = str(songID)+"-other")
			# sendLinks += "Looking for different Artist?:\n"+link+"\n\n"
			#
			# answer = ":lyrics:"+str(songID)
			# link = self.api.genLink(origin, answer, newLink = str(songID)+"-lyrics")
			# sendLinks += "Get Chords: "+link+"\n"
			#
			# answer = ":danilator:"+str(songID)
			# link = self.api.genLink(origin, answer, newLink = str(songID)+"-danilator")
			# sendLinks += "Lyric Translation: "+link+"\n"
			#
			# answer = ":chords:"+str(songID)
			# link = self.api.genLink(origin, answer, newLink = str(songID)+"-chords")
			# sendLinks += "Get Chords: "+link+"\n"
			seeMore = "See More - "+history[songID]["title"]
			time.sleep(1.5)
			self.api.send(origin, sendLinks, thumnail = thumnail = {"imageurl":None,"title":seeMore,"desc":"Other Artists, Covers, Lyrics, Chords","link":link+":more"}
)
			time.sleep(1.5)
			self.backup()

	def backup(self):
		self.api.backup(self.db)

	def updateDB(self, db):
		self.db = db
		# self.db = User.jsonUsersToUsers(db)

	def welcomeUser(self, origin):
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		if "users" not in self.db:
			self.db["users"] = {}
		if origin not in self.db["users"]:
			self.db["users"][origin] = origin
			self.backup()
