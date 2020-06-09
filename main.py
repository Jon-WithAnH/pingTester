# PepeLeave

"""
V3: Added date support and sound on error. Added default gateway finder instead of typing it in.
V3.1: Added a last disconnect.
v3.2: Added a one time line that shows the date. Optimized code. Fixed bugs. Added a small debug screen.
v4.0 i feel like i'm dumpster diving...
"""

import gatewayGrabber, subprocess, re, os
import datetime, time
import winsound

class interface:
    routerAddress = ""

    def __init__(self, outboundIP, pingsToDisplay, highPingThreshold):
        if not os.path.isdir("Logs"):
            print("First time setup")
            os.mkdir('Logs')
        self.ip=outboundIP
        self.pingsToDisplay = pingsToDisplay
        self.highPingThreshold = highPingThreshold
        self.routerAddress = gatewayGrabber.routerTester().localIP
        self.prevNums = []
        self.avgNum = 0
        self.highestPing = 0
        self.lastDisconnect = "none\n"
        os.chdir('Logs')  # For logging into the Logs subfolder
        self.looper()

    # Handles direct pinging, passes results and ip to display and list manager
    def pinger(self, ip):
        commandOutput = str(subprocess.check_output('ping -n 1 ' + ip))
        ping = int((re.search('time(\D)(\d+)', commandOutput)).group(2))  # 0 = time, 1 = <|=, 2 = digits
        if ip == self.routerAddress:
            self.display(ping, ip)
            # doesn't display or record pings to router. if ping is successful, it will be super low
            # failures still get logged
        else:
            self.prevPingManager(ping), self.display(ping, ip)
        if ping >= self.highPingThreshold: # threshold passed. needs to be logged
            self.logHighPing(ping, ip)
        return ping, ip

    # keeps track of previous ping stuff
    def prevPingManager(self, ping):
        if ping > self.highestPing:
            self.highestPing = ping
        # --- List management ---
        prevNums = self.prevNums
        if len(prevNums) <= self.pingsToDisplay:  # Adds the pings to the list for averaging and printing
            prevNums.append(ping)
        elif len(prevNums) > self.pingsToDisplay:  # Removes first entry and replaces it with the new one
            del prevNums[0]
            prevNums.append(ping)
        self.avgNum = int(sum(prevNums) / len(prevNums))


    def display(self, ping, ip):
        os.system('cls')
        print('PingTester to ' + ip)
        print('Highest ping: %sms' % self.highestPing)
        print('Avg ping: %sms' % self.avgNum)
        for pings in self.prevNums:  # Prints previous pings stored in prevNums
            print(pings, 'ms', sep='')
        print('\n\n\nLast disconnect: %s' % self.lastDisconnect, end='')

    def looper(self):
        ip=self.ip
        while True:
            try:
                self.pinger(ip)
            except subprocess.CalledProcessError: # Log and check router connection
                winsound.PlaySound("!", winsound.SND_ASYNC) # Audio notifier
                self.createLogFile(ip)
                while True: #pointless to reping google when router is down. keeps checking until router is up
                    try:
                        self.pinger(self.routerAddress)
                        break
                    except subprocess.CalledProcessError:
                        self.createLogFile(self.routerAddress)
                        time.sleep(1)
            time.sleep(1)


    def getTime(self):
        # 24 hr time
        return datetime.datetime.now()

    # Called by pinger should ping ever be higher than value of highPingThreshold in config
    def logHighPing(self, ping, ip):
        print("High ping logged")
        dayAndTime = self.getTime()
        fd = open(dayAndTime.date().__str__() +'.txt', mode='a')
        fd.write('WARNING: high ping of [%s] occurred @ %s:%s:%s to address %s\n' %
                 (ping, dayAndTime.hour, dayAndTime.minute, dayAndTime.second, ip))
        fd.close()

    # Actually just logs, idk why it's called "create"
    def createLogFile(self, ip):
        print("Connection Error occurred and logged %s" % ip)
        dayAndTime = self.getTime()
        fd = open(dayAndTime.date().__str__() +'.txt', mode='a')
        fd.write('Error occured @ %s:%s:%s to address %s\n' % (dayAndTime.hour, dayAndTime.minute, dayAndTime.second, ip))
        fd.close()
        self.lastDisconnect = str(dayAndTime.time().hour) + ":" + str(dayAndTime.time().minute) + ":" + str(dayAndTime.time().second)


if not os.path.exists('config.txt'):
    input("Fucking idiot, config not found. program will close")

with open('config.txt', mode='r') as config:
    defaultIP = (re.search("defaultIP=(.+)", config.readline())).group(1)
    pingsToDisplay = (re.search("pingsToDisplay=(.+)", config.readline())).group(1)
    highPingThreshold = (re.search("highPingThreshold=(.+)", config.readline())).group(1)
obj = interface(defaultIP, int(pingsToDisplay), int(highPingThreshold))
