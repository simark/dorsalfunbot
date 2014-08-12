import youtubelib

class Youtube:
	def __init__(self, irc):
		self.irc = irc

	def on_chanmsg(self, from_, chan, msg):
		ids = youtubelib.extract_yt_ids(msg)
		for i in ids:
			data = youtubelib.get_video_data(i)
			if not data:
				continue
			duration_string = ''
			duration = data['duration']
			if duration[0] > 0:
				duration_string += '{}:'.format(duration[0])
			duration_string += '{}:{:02}'.format(duration[1], duration[2])
			title = data['title']
			self.irc.privmsg(chan, '{} ({})'.format(title, duration_string))
