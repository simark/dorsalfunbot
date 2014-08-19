import mechanicalsoup
import requests
import json


class Xkcd:

    def __init__(self, irc):
        self.irc = irc

    def find_todays_xkcd(self, chan):
        comic_meta = requests.post('http://xkcd.com/info.0.json')
        data = json.loads(comic_meta.text)
        title = data['safe_title']
        number = data['num']
        text = '{} : http://xkcd.com/{}'.format(title, number)
        self.irc.privmsg(chan, text)

    def find_relevant_xkcd(self, chan, query):
        br = mechanicalsoup.Browser()
        targeturl += 'http://relevantxkcd.appspot.com/process?action=xkcd&query={}'.format(
            query)
        response = br.get(targeturl)
        extract = response.soup.text
        data = extract.split()
        comics_id = data[2::2]

        if len(comics_id) > 3:
            end = 3
        else:
            end = len(comics_id)

        for x in range(0, end):
            comic_meta = requests.post(
                'http://xkcd.com/{}/info.0.json'.format(comics_id[x]))
            if comic_meta.status_code == 404:
                self.irc.privmsg(
                    chan, "There seems to be some issue getting the relevant xkcd..")
            else:
                title = json.loads(comic_meta.text)['safe_title']
                text = '{} : http://xkcd.com/{}'.format(
                    title, comics_id[x])
                self.irc.privmsg(chan, text)

    def on_chanmsg(self, from_, chan, msg):
        data = msg.split()[1:]
        if len(data) == 0:
            self.find_todays_xkcd(chan)
        else:
            query = ''
            query = " ".join(data)
            self.find_relevant_xkcd(chan, query)

    def halp(self):
        return ["!xkcd :  Without an argument, it will give today's comic. Else, it takes query and prints relevant comics"]
