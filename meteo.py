import httplib2
import re
import bs4


class Meteo:

    def __init__(self, irc):
        self.irc = irc

    def on_chanmsg(self, from_, chan, msg):
        meteo = Meteo._get_meteo()
        if (meteo == None):
            self.irc.privmsg(chan, "impossible d'obtenir la météo...")
        else:
            self.irc.privmsg(
                chan, '{} °C - {}'.format(meteo['temp'], meteo['cond']))
            self.irc.privmsg(
                chan, '    humidité :   {} %'.format(meteo['humid']))
            self.irc.privmsg(
                chan, '    vent :       {} km/h'.format(meteo['wind']))
            self.irc.privmsg(
                chan, '    pression :   {} kPa ({})'.format(meteo['press'], meteo['tend']))
            self.irc.privmsg(
                chan, '    visibilité : {} km'.format(meteo['vis']))

            self.irc.privmsg(
                chan, '')
            self.irc.privmsg(
                chan, 'Messages du Gouvernement du Canada:')

            for msg in meteo['messages']:
                self.irc.privmsg(
                    chan, '* {}'.format(msg[0]))
                self.irc.privmsg(
                    chan, '    {}'.format(msg[1]))


    def _get_part(regex, content):
        m = re.search(regex, content)
        if (m == None):
            raise RuntimeError('aucun match d\'expression régulière')

        return m.group(1).strip()

    def _get_meteo():
        # il y a probablement une API quelque part pour ça, mais
        # c'est plus rapide pour moi de coder ça et c'est déjà
        # bien formaté en français ;-)
        meteo = {}
        try:
            # téléchargement de la page
            h = httplib2.Http()
            resp, content = h.request(
                'http://meteo.gc.ca/city/pages/qc-147_metric_f.html')
            if (resp.status != 200):
                raise RuntimeError('le statut de réponse HTTP n\'est pas 200')
            content = content.decode('utf-8')

            # température (°C)
            meteo['temp'] = Meteo._get_part(
                'ature.*</dt>\s*<dd[^>]*>\s*(-?[\d,]+)', content)

            # condition
            meteo['cond'] = Meteo._get_part(
                'ition.*</dt>\s*<dd[^>]*>(.+)</dd>', content)

            # pression (kPa)
            meteo['press'] = Meteo._get_part(
                'ression.*</dt>\s*<dd[^>]*>\s*([\d,]+)', content)

            # humidité (%)
            meteo['humid'] = Meteo._get_part(
                'midit.*</dt>\s*<dd[^>]*>\s*([\d,]+)', content)

            # vent (km/h)
            meteo['wind'] = Meteo._get_part(
                '[Vv]ent.*</dt>\s*<dd[^>]*>([^<]+)', content)

            # visibilité (km)
            meteo['vis'] = Meteo._get_part(
                'isibilit.*</dt>\s*<dd[^>]*>\s*([\d,]+)', content)

            # tendance
            meteo['tend'] = Meteo._get_part(
                'endance.*</dt>\s*<dd[^>]*>(.+)</dd>', content)
            meteo['messages'] = []

#            soup = bs4.BeautifulSoup(content, "html.parser")
#
#            nttvs = soup.find('aside', class_='gc-nttvs')
#            links = nttvs.find_all('a')
#            for l in links:
#                href = 'http://meteo.gc.ca' + l['href']
#                text = l.find('h3').text
#                meteo['messages'].append((text, href))

            return meteo
        except Exception as e:
            print(e)
            return None

    def halp(self):
        return "!meteo : rapporte les conditions météorologiques actuelles de Montréal"
