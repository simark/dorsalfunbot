class Fun:
	def __init__(self, irc):
		self.irc = irc

	def on_chanmsg(self, from_, chan, msg):
		self.irc.privmsg(chan, from_[0] + " has fun !")

	def halp(self):
		return "Avoir du fuuuuun!"
