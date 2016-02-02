import mpd
import subprocess


class Music:

    def __init__(self, irc):
        self.irc = irc

    def halp(self):
        return ["!music current", "!music youtube <youtube-link>"]

    def action_current(self, from_, chan, parts):
        client = mpd.MPDClient()
        client.connect('localhost', 6600, timeout=4)
        song = client.currentsong()

        client.disconnect()

        disp = song['artist'] + " - " + song['title']
        self.irc.privmsg(chan, disp)

    def action_search(self, from_, chan, parts):
        client = mpd.MPDClient()
        client.connect('localhost', 6600, timeout=4)
        result = client.search(parts[0], " ".join(parts[1:]))

        client.disconnect()

        for entry in result:
            self.irc.privmsg(from_[0], entry['file'])

    def action_download(self, from_, chan, parts):
        url = parts[0]
        try:
            subprocess.check_call(
                ["transmission-remote", "-n", "simark:test", "-w", "/home/simark/music/mount/music", "-a", url])
            self.irc.privmsg(chan, from_[0] + ": Started download")
        except subprocess.CalledProcessError:
            self.irc.privmsg(chan, from_[0] + ": Error trying to download")

    def action_youtubeplay(self, from_, chan, parts):
        url = parts[0]

        video = subprocess.check_output(
            ["/usr/local/bin/youtube-dl", "-f", "34", "-g", url], universal_newlines=True).split()[0]

        client = mpd.MPDClient()
        client.connect('localhost', 6600, timeout=4)

        result = client.add(video)

        status = client.status()
        # if (status['state'] == 'stop') :
        #    client.play(status['nextsong'])

        liste = client.playlist()
        if ('song' in status):
            currentSong = int(status['song'])
            client.move(len(liste) - 1, currentSong + 1)
        else:
            client.play(len(liste) - 1)
        # client.play(len(liste)-1)

        client.disconnect()

        self.irc.privmsg(chan, "okidoo")

    def on_chanmsg(self, from_, chan, msg):
        parts = msg.split()
        parts.pop(0)

        command = parts.pop(0)

        if command == 'current':
            self.action_current(from_, chan, parts)
        elif command == 'search':
            self.action_search(from_, chan, parts)
        elif command == 'download':
            self.action_download(from_, chan, parts)
        elif command == 'youtube':
            self.action_youtubeplay(from_, chan, parts)
