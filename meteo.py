import httplib2
import re
import codecs

class Meteo:
	def __init__(self, irc):
		self.irc = irc

	def on_chanmsg(self, from_, chan, msg):
		meteo = Meteo._get_meteo()
		if (meteo == None):
			self.irc.privmsg(chan, "impossible d'obtenir la météo...")
		else:
			self.irc.privmsg(chan, '{} °C ({}) - {}'.format(meteo['temp'], meteo['tend'], meteo['cond']))
			self.irc.privmsg(chan, '    humidité :   {} %'.format(meteo['humid']))
			self.irc.privmsg(chan, '    vent :       {} km/h'.format(meteo['wind']))
			self.irc.privmsg(chan, '    pression :   {} kPa'.format(meteo['press']))
			self.irc.privmsg(chan, '    visibilité : {} km'.format(meteo['vis']))
	
	def _get_part(regex, content):
		m = re.search(regex, content)
		if (m == None):
			raise
		
		return m.group(1).strip()
	
	def _get_meteo():
		# il y a probablement une API quelque part pour ça, mais
		# c'est plus rapide pour moi de coder ça et c'est déjà
		# bien formaté en français ;-)
		meteo = {}
		try:
			# téléchargement de la page
			h = httplib2.Http()
			resp, content = h.request('http://meteo.gc.ca/city/pages/qc-147_metric_f.html')
			if (resp.status != 200):
				raise
			content = content.decode('utf-8')
			
			# température (°C)
			meteo['temp'] = Meteo._get_part('ature.*</dt>\s*<dd>\s*([\d,]+)', content)
			
			# condition
			meteo['cond'] = Meteo._get_part('ition.*</dt>\s*<dd>(.+)</dd>', content)
			
			# pression (kPa)
			meteo['press'] = Meteo._get_part('ression.*</dt>\s*<dd>\s*([\d,]+)', content)
			
			# humidité (%)
			meteo['humid'] = Meteo._get_part('midit.*</dt>\s*<dd>\s*([\d,]+)', content)
			
			# vent (km/h)
			meteo['wind'] = Meteo._get_part('[Vv]ent.*</dt>\s*<dd.*?>([^<]+)', content)
			
			# visibilité (km)
			meteo['vis'] = Meteo._get_part('isibilit.*</dt>\s*<dd>\s*([\d,]+)', content)
			
			# tendance
			meteo['tend'] = Meteo._get_part('endance.*</dt>\s*<dd>(.+)</dd>', content)
			
			return meteo
		except:
			return None

	def halp(self):
		return "conditions météorologiques actuelle";
