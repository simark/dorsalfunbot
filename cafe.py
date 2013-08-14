
from bs4 import BeautifulSoup
import http.client
import datetime
import unidecode
import schedule

def EatSpaces(s):
	new_s = s.replace('  ', ' ')
	while new_s != s:
		s = new_s
		new_s = s.replace('  ', ' ')

	return s.strip()

def ObtainTodaysMenu(today):
	conn = http.client.HTTPConnection("www.polymtl.ca")
	req = conn.request("GET", "/vie/cafe/")
	page = conn.getresponse().read()

	b = BeautifulSoup(page)

	menu = [[], [], [], [], [], []]

	divContenu = b.find("div", id = "contenu-texte")
	rows = divContenu.find_all("tr")
	rows.pop(0)

	for row in rows:
		cells = row.find_all("td")
		for (i, cell) in zip(range(6), cells):
			text = EatSpaces(cell.get_text().capitalize())
			menu[i].append(text)

	titresPlats = menu.pop(0)

	if today < len(menu):
		return zip(titresPlats, menu[today])
	else:
		return None

class Cafe:
	def __init__(self, irc):
		self.irc = irc
		self.scheduler = schedule.Scheduler()
		self.job = self.scheduler.every().day.at("11:45").do(self.print_manger)
		self.cease = self.scheduler.run_continuously()


	def dispose(self):
		self.scheduler.clear()
		self.cease.set()
		pass

	def print_manger(self):
		now = datetime.datetime.now()
		now = now.strftime("%Y-%m-%d %H:%M:%S")
		print(now + " JE VEUX MANGER!")
		self.irc.privmsg("#dorsal-fun", "C'est le temps de manger!")
		now = datetime.datetime.now()
		now = now.strftime("%Y-%m-%d %H:%M:%S")
		print(now + " OMNOMNOM")

	def action_getmenu(self, from_, chan, parts):
		menu = None
		s = "Je ne comprends pas :("
		jours = {"lundi": 0, "mardi": 1, "mercredi": 2, "jeudi": 3, "vendredi": 4, "samedi": 5, "dimanche": 6}
		today = datetime.datetime.now().weekday()
		tomorrow = (today + 1) % 7
		if len(parts) > 0:
			if parts[0] in jours:
				menu = ObtainTodaysMenu(jours[parts[0]])
			elif parts[0] == "demain":
				menu = ObtainTodaysMenu(tomorrow)
			elif parts[0] == "ericsson":
				s = "Club sandwich!"
		else:
			menu = ObtainTodaysMenu(today)

		if menu:
			s = ', '.join([hey + ": " + ho for (hey, ho) in menu])

		#Replace unicode apostrophe with latin-1 compatible
		s.replace("\u2019", "'")

		self.irc.privmsg(chan, s.encode("latin-1", errors="ignore").decode("latin-1"))

	def on_chanmsg(self, from_, chan, msg):
		parts = msg.split()[1:]
		self.action_getmenu(from_, chan, parts)

	def halp(self):
		return ["!menu: get today's menu"]


