import mechanicalsoup
import requests
import json

def shorten(url):
	post_url = 'https://www.googleapis.com/urlshortener/v1/url'
	postdata = {'longUrl':url}
	headers = {'Content-Type':'application/json'}
	ret = requests.post(post_url, data=json.dumps(postdata), headers=headers)
	return json.loads(ret.text)['id']

class Publish:
	def __init__(self, irc):
        	self.irc = irc

	def generate_paper(self, chan, authors):
		br = mechanicalsoup.Browser()
		# names = ['Simon Marchi', 'Suchakra Sharma', 'Francis']
		# Padding the list
		if len(authors) > 5 or len(authors) == 0:
			self.irc.privmsg(chan, "The number of authors.. is too damn high!") 
		else :
			authors += [''] * (5 - len(authors))

			targeturl = ''
			targeturl += 'http://pdos.csail.mit.edu/cgi-bin/sciredirect.cgi?author={}&author={}&author={}&author={}&author={}'.format(authors[0], authors[1], authors[2], authors[3], authors[4])
			responsepage = br.get(targeturl)
			title = responsepage.soup.title.text
			links = []
			for a in responsepage.soup.findAll('a', href=True):
				link = a['href']	
				if 'pdf' in link:
					pdfurl = 'http://apps.pdos.lcs.mit.edu'+link
					url = shorten(pdfurl)
			if (url == None):
				self.irc.privmsg(chan, "This is immoral! I can't bear the burden of this..")
			else:
				self.irc.privmsg(chan, title+" : "+url)
				
	def on_chanmsg(self, from_, chan, msg):
		authors = msg.split(',')[0:]
		first = authors[0].split()
		first.remove(first[0])
		authors[0] = " ".join(first)
		self.generate_paper(chan, authors)

	def halp(self):
        	return ["!publish Albert Einstein, Nikola Tesla, Thomas Edison"]
