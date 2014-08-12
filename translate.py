import goslate
import globals

class Translate:
	def __init__(self, irc):
		self.irc = irc

	def on_chanmsg(self, from_, chan, msg):
		translated = Translate.get_translation()
		if (translated == None):
			self.irc.privmsg(chan, "Could not translate...")
		else:
			self.irc.privmsg(chan, "En Anglais : " + translated)
	
	def get_translation():
		try:
			gs = goslate.Goslate()
			trans_text = gs.translate(globals.g_buffmsg, 'en')
			return trans_text
		except:
			return None

	def halp(self):
		return "!translate : Translate last statement to English";
