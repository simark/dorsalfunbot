import subprocess

class Sound:
	def __init__(self, irc):
		self.irc = irc
		self.people = {"scientist":"yannick.wav","simark":"good2.wav","XaF":"raphael.wav","suchakra":"suchakra.wav"}
		self.text = {"good":"good2.wav", "super":"superbe1.wav"}

	def on_chanmsg(self, from_, chan, msg):
		if from_[0] in self.people:
			subprocess.call(["aplay", "/home/simark/audio_samples/"+self.people[from_[0]]])
		for word in self.text:
			if word in msg:
				subprocess.call(["aplay", "/home/simark/audio_samples/"+self.text[word]])
