class Help:
	def __init__(self, irc):
		self.irc = irc

	def on_chanmsg(self, from_, chan, msg):
		self.irc.privmsg(from_[0], "There is no help right now !")
