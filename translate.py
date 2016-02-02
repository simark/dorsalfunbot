import globals
from mstranslator import Translator


class Translate:

    def __init__(self, irc):
        self.irc = irc

    def on_chanmsg(self, from_, chan, msg):
        parts = msg.split(maxsplit=1)

        if len(parts) > 1:
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
            t = Translator('dorsalfunbot', 'lWJjt3W86DqQX5J+VGCDsvD3LU9/eZFvG0VQj4k6J/Y=')
            from_lang = t.detect_lang(to_translate)
            if from_lang == 'en':
                to_lang = 'fr'
                header = 'en -> fr:'
            else:
                to_lang = 'en'
                header = '{} -> en:'.format(from_lang)
            trans_text = t.translate(to_translate, lang_from=from_lang, lang_to=to_lang)
            return '{} {}'.format(header, trans_text)
        except Exception as e:
            print("Translation error: {}".format(e))
            return None

    def halp(self):
        return ['Translate English text to French, or other languages to English.',
                '!translate: Translate last statement.',
                '!translate <text>: Translate <text>.']
