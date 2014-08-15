import goslate
import globals


class Translate:

    def __init__(self, irc):
        self.irc = irc

    def on_chanmsg(self, from_, chan, msg):
        translated = Translate.get_translation()
        if (translated == None):
            self.irc.privmsg(chan, "Could not translate...")
        else:
            self.irc.privmsg(chan, translated)

    def get_translation():
        try:
            gs = goslate.Goslate()
            from_lang = gs.detect(globals.g_buffmsg)
            if from_lang == 'fr':
                to_lang = 'en'
                header = 'Fr -> En : '
            elif from_lang == 'en':
                to_lang = 'fr'
                header = 'En -> Fr : '
            else:
                to_lang = 'en'
                header = '{} -> En : '.format(from_lang)
            trans_text = gs.translate(globals.g_buffmsg, to_lang)
            return header + trans_text
        except:
            return None

    def halp(self):
        return "!translate : Translate last statement to English"
