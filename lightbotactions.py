import RPi.GPIO as GPIO

valid_target = {'0': 15, '1': 16, '2': 11, '3': 12}
valid_state = {'on': GPIO.HIGH, 'off': GPIO.LOW}

class LightbotActions:
	def __init__(self, irc):
		GPIO.setmode(GPIO.BOARD)
		for x in valid_target:
			GPIO.setup(valid_target[x], GPIO.OUT)
		self.irc = irc

	def action_light_turn(self, from_, chan, msg, parts):
		if len(parts) != 2:
			return
		
		target = parts[0]
		state = parts[1]

		if target not in valid_target or state not in valid_state:
			return

		value = valid_state[state]
		pin = valid_target[target]
		GPIO.output(pin, value)
		self.irc.privmsg(chan, "Light " + target + " is now " + state)

	def action_light_status(self, from_, chan, msg, parts):
		if len(parts) == 0:
			for t in sorted(valid_target.keys()):
				value = "on" if GPIO.input(valid_target[t]) else "off"
				self.irc.privmsg(chan, "Light " + str(t) + ": " + value)
		elif len(parts) == 1:
			t = parts[0]
			if t in valid_target:
				value = "on" if GPIO.input(valid_target[t]) else "off"
				self.irc.privmsg(chan, "Light " + str(t) + ": " + value)
		

	def action_light(self, from_, chan, msg, parts):
		if len(parts) == 0:
			return
		
		cmd = parts.pop(0)

		if cmd == 'turn':
			self.action_light_turn(from_, chan, msg, parts)
		elif cmd == 'status':
			self.action_light_status(from_, chan, msg, parts)

	def on_chanmsg(self, from_, chan, msg):
		parts = msg.split()[1:]
		self.action_light(from_, chan, msg, parts)
