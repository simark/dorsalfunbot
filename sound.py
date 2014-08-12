import subprocess
import time
import yaml


class Sound:

    def __init__(self, irc):
        with open("sound.yaml") as configfile:
            self.config = yaml.load(configfile)

        self.irc = irc
        self.people = self.config["people"]
        self.people_cooldown = {}
        self.people_lastuse = {}
        for person in self.people:
            self.people_cooldown[person] = self.config[
                "config"]["default_people_cooldown"]
            self.people_lastuse[person] = 0
        self.text = self.config["words"]
        self.text_cooldown = {}
        self.text_lastuse = {}
        for word in self.text:
            self.text_cooldown[word] = self.config[
                "config"]["default_word_cooldown"]
            self.text_lastuse[word] = 0

    def on_chanmsg(self, from_, chan, msg):
        print(from_)
        current_time = time.time()
        if from_[0] in self.people:
            if current_time > self.people_lastuse[from_[0]] + self.people_cooldown[from_[0]]:
                subprocess.call(
                    ["aplay", "/home/simark/audio_samples/" + self.people[from_[0]]])
                self.people_lastuse[from_[0]] = current_time
        for word in self.text:
            if word in msg.lower():
                if current_time > (self.text_lastuse[word] + self.text_cooldown[word]):
                    subprocess.call(
                        ["aplay", "/home/simark/audio_samples/" + self.text[word]])
                    self.text_lastuse[word] = current_time
