import pingTester, gatewayGrabber
import re, os
import time

# Creates config file is it doesn't exist
if not os.path.exists('config.txt'):
    with open('config.txt', mode='w') as config:
        config.write('''defaultIP=8.8.8.8\npingsToDisplay=10\nhighPingThreshold=100''')

if not os.path.isdir("Logs"):
    os.mkdir('Logs')

# pulls user variables from config
with open('config.txt', mode='r') as config:
    defaultIP = (re.search("\d.+", config.readline())).group(0)
    pingsToDisplay = int((re.search("\d+", config.readline())).group(0))
    highPingThreshold = int((re.search("\d+", config.readline())).group(0))


class combine():
    def __init__(self, outbound, router):
        self.outbound = outbound
        self.router = router

    def start(self):
        while len(self.outbound.prevNums) < self.outbound.pingsToDisplay+1:
            # i have no clue what will happen if outbound is successful but router fails.
            # i think the check in the display loop with catch it. not sure tho. dunno how to create that problem easily
            # anyways, start operations. generating data
            self.outbound.pinger()
            self.router.pinger()
            self.display()
            time.sleep(.5)
        while True:
            time.sleep(1)
            if not self.outbound.pinger():
                # outbound ping failed
                while not self.router.pinger():
                    # router is down
                    print("Connection to router failed. Time between router pings is 4 seconds. Please check connection")
                    time.sleep(4)
            self.display()

    # could ping one and then ping the other during first 10 tests. after that only ping outbound
    # reduce sleep to .5 to make up for that
    def display(self):
        x=80
        os.system('cls')
        print(('PingTester to ' + self.outbound.ip).ljust(x) + "PingTester to " + self.router.ip)
        print(('Highest ping: %sms' % self.outbound.highestPing).ljust(x) + "Highest ping: %sms" % self.router.highestPing)
        print(('Avg ping: %sms' % self.outbound.avgNum).ljust(x) + "Avg ping: %sms" % self.router.avgNum)
        # if outbound succeeds but router fails, there will be an IndexOutOfBound
        if len(self.outbound.prevNums) <= len(self.router.prevNums):
            for pings in range(len(self.outbound.prevNums)):
                print(("%sms" % self.outbound.prevNums[pings]).ljust(x) + "%sms" % self.router.prevNums[pings])
        print('\n\n\nLast disconnect: %s' % self.outbound.lastDisconnect, end='')


os.chdir('Logs')  # For logging into the Logs subfolder
outboundObj = pingTester.interface(defaultIP, int(pingsToDisplay), int(highPingThreshold))
routerObj = pingTester.interface(gatewayGrabber.routerTester().localIP, pingsToDisplay, 20)

combine(outboundObj, routerObj).start()
