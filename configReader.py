import os
import re
import sys
from traceback import print_exc as printStackTrace

class configInterface():

    def __init__(self):
        self.defaultIP = ""
        self.secondIP = ""
        self.thirdIP = ""
        self.pingsToDisplay = 0
        self.highPingThreshold = 0

    def _createConfig(self):
        with open('config.txt', mode='w') as config:
            config.write(
                        '''; To create new IP's to ping, add another line above the pingsToDisplay variable\n; and just type "=x.x.x.x" where x is the value of the ip bits. The name doesn't matter.\n\n'''
                        '''defaultIP=8.8.8.8\n\n\n'''
                        '''pingsToDisplay=10\n'''
                        '''highPingThreshold=100\n''')
        # we'll want to reread the configs to the obj values here so that they will automatically be read
        self.readConfig()

    def readConfig(self):
        if not os.path.exists('config.txt'):  # initial start up
            print("ConfigReader.readConfig(): Config file not found. Generating...",
                  file=sys.stderr, flush=True)
            self._createConfig()
        with open('config.txt', mode='r') as config:
                tmp = re.findall("=([^x].+)", config.read())
                if len(tmp) < 2:
                    print(f"usage: config does not match minimum requirements. "
                          f"Delete config.txt and rerun program to reset file\n")
                    if input("Regenerate config? (y/n) ").lower() == "y":
                        self._createConfig()
                    else:
                        exit(-1)

                self.defaultIP = tmp[0]
                self.pingsToDisplay = tmp[-2]
                self.highPingThreshold = tmp[-1]

