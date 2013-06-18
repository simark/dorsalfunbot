import re

class Crazy:
	def __init__(self, irc):
		self.irc = irc
		self.max_lvl = 11
	
	def usage(self, chan, from_):
		self.irc.privmsg(chan, from_[0] + ": the crazyness level must be an int from 0 to " + str(self.max_lvl))
		

	def on_chanmsg(self, from_, chan, msg):
		parts = msg.split()
		if len(parts) != 2:
			self.usage(chan, from_)
			return

		level_str = parts[1]
		topic = self.irc.topic(chan)[0]

		try:
			current_level = len(re.findall("\[(=*)-*\]", topic)[0])
		except IndexError:
			current_level = 0
			not_found = True

		if level_str == "++":
			if current_level < self.max_lvl:
				level = current_level + 1
			else:
				level = current_level
		elif level_str == "--":
			if current_level > 0:
				level = current_level - 1
			else:
				level = current_level
		else:

			try:
				level = int(level_str)
				if level < 0 or level > self.max_lvl:
					self.usage(chan, from_)
					return
			except ValueError:
				self.usage(chan, from_)
				return		
		crazy_str = "[" + "=" * level  + "-" * (self.max_lvl - level) + "]"
		new_topic = re.sub("(\[=+-+\]|\[=+\]|\[-+\])", crazy_str, topic)
		#self.irc.privmsg(chan, "New topic would be " + new_topic)
		try:
			self.irc.topic(chan, new_topic)
		except ChanOPrivsNeeded:
			self.irc.privmsg(chan, "I require OP, OP, OP")


