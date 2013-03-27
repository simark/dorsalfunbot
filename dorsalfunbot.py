import lurklib
import lightbotactions
import imp

class DorsalFunBot(lurklib.Client):
	def __init__(self, *args, **kwargs):
		super(DorsalFunBot, self).__init__(*args, **kwargs)
		self.actions = lightbotactions.LightbotActions(self)

	def on_connect(self):
		print("connected")
		self.join_('#dorsal-fun')

	def on_chanmsg(self, from_, chan, msg):
		parts = msg.split()
		action = parts.pop(0)

		if action == '!light':
			self.actions.on_chanmsg(from_, chan, msg)

	def on_privnotice(self, from_, notice):
		if notice == "rehash":
			imp.reload(lightbotactions)
			self.actions = lightbotactions.LightbotActions(self)
			self.notice(from_[0], "Modules reloaded")


if __name__ == '__main__':
	bot = DorsalFunBot(server = 'irc.oftc.net', nick='DorsalFunBot', user='DorsalFunBot')
	bot.mainloop()
