#Service.py
import time
import spotipy
import spotipy.util as util
from youtube_search import YoutubeSearch

class MusicService(object):
	id = "Music"
	name = "🔊 Music 🔊"
	welcome = "Welcome to Music 🔊 Service \nSend us a song to get Youtube and Spotify Links :)"
	help = "send a message to get it back"
	share = None

	def __init__(self,db, api):
		MusicService.share = self

		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Echo",MusicService.share)
		self.db = db
		self.api = api
		if "upcoming" not in self.db:
			self.db["upcoming"] = []
		if "users" not in self.db:
			self.db["users"] = {}

		self.spotify = None
		try:
			token = spotipy.SpotifyClientCredentials(client_id ='d419f4fe1de143c0ab7561734322fbe2', client_secret='a5738d2f12a44336b74153cc96a1946e')
			cache_token = token.get_access_token()
			self.spotify = spotipy.Spotify(cache_token)
		except Exception as e:
			print("EEEEEEEEEEEEEE spotify init",e)

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

		# if user not in self.db["users"]:
		# 	self.db["users"][user] = user
		# 	self.api.send(origin, "WELCOME "+user)
		# 	self.backup()

		# self.db["upcoming"].append([origin, content])

		# query = "sweet child"
		sendBack = "Sorry we could not find your song on Spotify for some reason.\n"
		found = False
		try:
			results = self.spotify.search(content)
			if len(results) > 0:
				res = results['tracks']['items'][0]
				link = res['external_urls']['spotify']
				title = res["name"]
				artist = res["album"]["artists"][0]["name"]
				found = True
		except Exception as e:
			print("COULD NOT FIND SONG ON SPOTIFY", e)

		search = content
		if found:
			sendBack = "*"+title+" - "+artist+"*\n"
			sendBack += link+"\n\n"
			search = title+" "+artist

		ytres = YoutubeSearch(search, max_results=1).to_dict()
		if ytres is not None and len(ytres) == 1:
			try:
				vidID = ytres[0]['url_suffix']
				if vidID is not None and len(vidID) > 0:
					sendBack+="https://youtu.be"+vidID

			except Exception as e:
				print("COULD NOT FIND SONG ON YOUTUBE", e)


		self.api.send(origin, sendBack)

	def backup(self):
		self.api.backup(self.db)

	def updateDB(self, db):
		self.db = db
		# self.db = User.jsonUsersToUsers(db)
