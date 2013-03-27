import lurklib
import lightbotactions
import imp
import yaml
import sys

class DorsalFunBot(lurklib.Client):
	def __init__(self, config):
		super(DorsalFunBot, self).__init__(**config['irc'])
		self.modules = {}
		self.load_modules(config['modules'])
	
	def load_modules(self, moduleslist):
		try:
			modules = {}
			for module in moduleslist:
				try:
					if module["action"] in modules:
						modinfo = imp.find_module(module["name"])
						modload = imp.load_module(module["name"], *modinfo)
						modules[module["action"]] = getattr(modload, module["class"])(self)
						print("Loaded module " + module['name'])
					else:
						print("Module "+module["name"]+" skipped as its action is already registered.")
				except ImportError as e:
					print(str(e))
			self.modules = modules
			return True
		except Exception as e:
			print(str(e))
			return False

	def on_connect(self):
		print("connected")
		for chan in config['channels']:
			self.join_(chan)

	def on_chanmsg(self, from_, chan, msg):
		action = msg.split(maxsplit=1)[0]

		if action[0] == "!" and action[1:] in self.modules:
			self.modules[action[1:]].on_chanmsg(from_, chan, msg)

	def on_privnotice(self, from_, notice):
		if notice == "rehash":
			config = load_config()
			if not config:
				self.notice(from_[0], "Error loading config file, no rehash has been done")
				return
			
			if self.load_modules(config['modules']):
				self.notice(from_[0], "rehash has been done")
			else:
				self.notice(from_[0], "rehash failed dramatically")

def load_config():
	try:
		with open("config.yaml") as configfile:
			config = yaml.load(configfile)
			check_config(config)
	except Exception as e:
		print("Error loading configuration file: "+str(e))
		return False
	return config


def check_config(config):
	if not 'irc' in config.keys():
		raise Exception("No IRC configuration found")
	elif not 'channels' in config.keys():
		raise Exception("No channels configuration found")
	elif not 'nick'     in config['irc'].keys() \
	  or not 'user'     in config['irc'].keys() \
	  or not 'server'  in config['irc'].keys():
	  	raise Exception("You need 'nick', 'user' and 'server' information in the configuration")

if __name__ == '__main__':
	config = load_config()
	if not config:
		sys.exit(1)

	bot = DorsalFunBot(config=config)
	bot.mainloop()
