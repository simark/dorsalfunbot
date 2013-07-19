import mpd
import re
import io
import urllib.request
import subprocess
import couteau
import datetime
import subprocess
import schedule
import unicodedata

class Cafe:
	def __init__(self, irc):
		self.irc = irc
		self.scheduler = schedule.Scheduler()
		self.job = self.scheduler.every().day.at("11:45").do(self.print_menu)
		self.cease = self.scheduler.run_continuously()


	def dispose(self):
		self.cease.set()


	def print_menu(self):
		#download menu image from cafe website

		#cut image

		#OCR

		#print results
		self.irc.privmsg("#dorsal-fun", "C'est le temps de manger!")


	def action_printmenu(self, from_, chan, parts):
		if len(parts) > 0:
			ocr = parts[0]
			menu = parseMenu(ocr)
		else:
			menu = parseMenu()

		print(menu)
		string = ", ".join(menu[:-1])+" et " + menu[-1]

		self.irc.privmsg(chan, string)


	def on_chanmsg(self, from_, chan, msg):
		parts = msg.split()[1:]
		self.action_printmenu(from_, chan, parts)	


def parseMenu(ocr="tesseract"):

	URL = "http://www.polymtl.ca/vie/cafe/"
	jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]

	response = urllib.request.urlopen(URL)

	string = response.read().decode(errors="ignore")

	#with io.open('cafe.html', 'r', encoding="ascii", errors="ignore") as file:
	#	str = file.read()

	result = re.findall("<img src=\"(.*?\.gif).*?/>", string)[0]
	print(result)

	response = urllib.request.urlopen(URL+result)

	with io.open("cafe.gif", "wb") as f:
		f.write(response.read())

	couteau.decouper("cafe.gif")

	jour = datetime.datetime.today().weekday()

	miam = []

	if jour < 5:
		for i in range(1,7):
			inputFile = jours[jour]+str(i)+".bmp"
			outputFile = jours[jour]+str(i)

			if ocr == "tesseract":
				subprocess.call(["tesseract", inputFile, outputFile, "-l", "fra"])
			elif ocr == "gocr":
				subprocess.call(["gocr", "-i", inputFile, "-o", outputFile+".txt"])
			else:
				return []

			with open(jours[jour]+str(i)+".txt", "r") as f:
				texte = f.read().replace("\n", " ").strip()
				texte = unicodedata.normalize("NFKD", texte).encode("latin-1", "ignore").decode()
				miam.append(texte)
	else:
		pass

	#print(miam)
	return miam

	#print(subprocess.check_call(["python2", "couteau.py", "cafe.gif"]))
