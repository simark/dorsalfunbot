import lurklib
import imp
import yaml
import sys
import subprocess
import os
import signal

import globals


class DorsalFunBot(lurklib.Client):

    def __init__(self, config):
        super(DorsalFunBot, self).__init__(**config['irc'])
        self.modules = {}
        self.load_modules(config['modules'])
        globals.init()

    def load_modules(self, moduleslist):
        try:
            modules = {}
            for module in moduleslist:
                try:
                    action = module["action"] if "action" in module else ""
                    if action not in modules:
                        modules[action] = []

                    modinfo = imp.find_module(module["name"])
                    modload = imp.load_module(module["name"], *modinfo)
                    modules[action].append(
                        getattr(modload, module["class"])(self))
                    print("Loaded module " + module['name'])
                except ImportError as e:
                    print(str(e))
            self.modules = modules
            return True
        except Exception as e:
            print(str(e))
            return False

    def unload_modules(self):
        for action in self.modules:
            for module in self.modules[action]:
                try:
                    module.dispose()
                    print("Disposed module " + module.__class__.__name__)
                except Exception as e:
                    pass

    def on_connect(self):
        print("connected")
        for chan in config['channels']:
            self.join_(chan)

    def on_chanmsg(self, from_, chan, msg):
        if "" in self.modules:
            for module in self.modules[""]:
                try:
                    module.on_chanmsg(from_, chan, msg)
                except Exception as e:
                    print("Error in module: " + str(e))
        try:
            action = msg.split(maxsplit=1)[0]

            helps = {}
            if action == "!help":
                for action in self.modules:
                    for module in self.modules[action]:
                        try:
                            halp = module.halp()
                            if not isinstance(halp, list):
                                halp = [halp]
                            helps[module.__class__.__name__] = halp
                        except Exception as e:
                            print("Error in module help: " + str(e))

                for m in helps:
                    self.privmsg(from_[0], m)
                    for msg in helps[m]:
                        self.privmsg(from_[0], "  " + str(msg))

            elif action[0] == "!" and action[1:] in self.modules:
                for module in self.modules[action[1:]]:
                    try:
                        module.on_chanmsg(from_, chan, msg)
                    except Exception as e:
                        print(
                            "Error in module " + module.__class__.__name__ + ": " + str(e))
            else:
                globals.g_buffmsg = msg
        except IndexError:
            pass

    def on_privnotice(self, from_, notice):
        if notice == "rehash":
            config = load_config()
            if not config:
                self.notice(
                    from_[0], "Error loading config file, no rehash has been done")
                return

            self.unload_modules()

            if self.load_modules(config['modules']):
                self.notice(from_[0], "rehash has been done")
            else:
                self.notice(from_[0], "rehash failed dramatically")


def load_config():
    try:
        with open("config.yaml") as configfile:
            config = yaml.load(configfile)
            check_config(config)
    except Exception as e:
        print("Error loading configuration file: " + str(e))
        return False
    return config


def check_config(config):
    if not 'irc' in config.keys():
        raise Exception("No IRC configuration found")
    elif not 'channels' in config.keys():
        raise Exception("No channels configuration found")
    elif not 'nick'     in config['irc'].keys() \
            or not 'user'     in config['irc'].keys() \
            or not 'server' in config['irc'].keys():
        raise Exception(
            "You need 'nick', 'user' and 'server' information in the configuration")

if __name__ == '__main__':
    config = load_config()
    if not config:
        sys.exit(1)

    pidfile = "/var/run/dorsalfunbot.pid"

    try:
        with open(pidfile, "r") as f:
            pid = int(f.read().strip())
            os.kill(pid, 0)
            print("Le bot est deja lance (pid %d)" % (pid))
            sys.exit(0)
    except ProcessLookupError as e:
        print("Le pid dans le fichier pid n'existe pas, go")
    except IOError as e:
        print("Le fichier pid n'existe pas, go " + str(e))
    except ValueError as e:
        print("Le fichier pid contient de la cochonnerie, go")

    with open(pidfile, "w") as f:
        pid = os.getpid()
        f.write(str(pid))

    bot = DorsalFunBot(config=config)
    while True:
        try:
            bot.mainloop()
        except InterruptedError as e:
            pass
        except:
            bot.unload_modules()
            break
