import os

class Amihot:
	def __init__(self, irc):
		self.irc = irc

	def on_chanmsg(self, from_, chan, msg):
		cputemp = Amihot.get_cpu_temp()
		if (cputemp == None):
			self.irc.privmsg(chan, "Can't determine my hotness...")
		else:
			self.irc.privmsg(chan, "CPU is at {}".format(cputemp)+u" \u2103")

	def get_cpu_temp():
		try:
			with open("/sys/class/thermal/thermal_zone0/temp") as f:
				content = str(f.readlines())
				temp = float(content.strip('[ ] \' \\n'))/1000
				return format("%.2f" % temp)
		except:
			return None

	def halp(self):
		return "!amihot : Get CPU temperature of Pi"
