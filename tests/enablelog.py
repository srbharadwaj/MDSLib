import logging


def banner(text, ch='=', length=78):
    spaced_text = ' %s ' % text
    banner = spaced_text.center(length, ch)
    print(banner)


class ScriptLog(object):
    def __init__(self, logfile,consolelevel=logging.INFO):
        logFormatter = logging.Formatter("[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s")
        self.log = logging.getLogger()

        fileHandler = logging.FileHandler(logfile)
        fileHandler.setFormatter(logFormatter)
        fileHandler.setLevel(logging.DEBUG)
        self.log.addHandler(fileHandler)
        self.log.setLevel(logging.DEBUG)

        self.consoleHandler = logging.StreamHandler()
        self.consoleHandler.setFormatter(logFormatter)
        self.consoleHandler.setLevel(consolelevel)
        self.log.addHandler(self.consoleHandler)
