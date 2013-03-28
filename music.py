import mpd

class Music:
	def __init__(self, irc):
		self.irc = irc

	def action_current(self, from_, chan, parts):
		client = mpd.MPDClient()
		client.connect('localhost', 6600, timeout = 4)
		song = client.currentsong()

		client.disconnect()

		disp = song['artist'] + " - " + song['title']
		self.irc.privmsg(chan, disp)

	def on_chanmsg(self, from_, chan, msg):
		parts = msg.split()
		parts.pop(0)
		
		command = parts.pop(0)

		if command == 'current':
			self.action_current(from_, chan, parts)
