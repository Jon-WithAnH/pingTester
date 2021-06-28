import re


class configInterface():

    def __init__(self):
        self.defaultIP = ""
        self.secondIP = ""
        self.thirdIP = ""
        self.pingsToDisplay = 0
        self.highPingThreshold = 0

    def createConfig(self):
        with open('config.txt', mode='w') as config:
            config.write('''defaultIP=8.8.8.8\n'''
                         '''secondIP=None\n'''
                         '''defaultIP=None\n'''
                         '''pingsToDisplay=10\n'''
                         '''highPingThreshold=100\n''')

    def readConfig(self):
        with open('config.txt', mode='r') as config:
            try:
                self.defaultIP = (re.search("\d.+", config.readline())).group(0)
                self.secondIP = (re.search("\d.+", config.readline())).group(0)
                self.thirdIP = (re.search("\d.+", config.readline())).group(0)
                self.pingsToDisplay = int((re.search("\d+", config.readline())).group(0))
                self.highPingThreshold = int((re.search("\d+", config.readline())).group(0))
            except AttributeError as ex:
                print(f"usage: config does not match minimum requirements. "
                      f"Delete config.txt and rerun program to reset file\n"
                      f"{repr(ex)}")
                if input("Regenerate config? (y/n) ").lower() == "y":
                    self.createConfig()
                else:
                    exit(-1)
