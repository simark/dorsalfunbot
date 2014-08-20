import goslate
import globals


class Translate:

    def __init__(self, irc):
        self.irc = irc

    def on_chanmsg(self, from_, chan, msg):
        parts = msg.split(max=1)

        # Remote !translate
        parts.pop(0)

        if len(parts) > 0:
            to_translate = parts[1]
        else:
            to_translate = globals.g_buffmsg

        translated = Translate.get_translation(to_translate)
        if (translated == None):
            self.irc.privmsg(chan, "Could not translate...")
        else:
            self.irc.privmsg(chan, translated)

    def get_translation(to_translate):
        try:
            gs = goslate.Goslate()
            from_lang = gs.detect(to_translate)
            if from_lang == 'en':
                to_lang = 'fr'
                header = 'en -> fr:'
            else:
                to_lang = 'en'
                header = '{} -> en:'.format(from_lang)
            trans_text = gs.translate(to_translate, to_lang)
            return '{} {}'.format(header, trans_text)
        except:
            return None

    def halp(self):
        return ['Translate English text to French, or other languages to English.',
                '!translate: Translate last statement.',
                '!translate <text>: Translate <text>.']
