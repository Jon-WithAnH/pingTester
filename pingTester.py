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
    # routerAddress = ""

    def __init__(self, outboundIP, pingsToDisplay, highPingThreshold):
        self.ip = outboundIP
        self.pingsToDisplay = pingsToDisplay
        self.highPingThreshold = highPingThreshold
        self.prevNums = []
        self.avgNum = 0
        self.highestPing = 0
        self.lastDisconnect = "none\n"

    # Handles direct pinging, passes results and ip to display and list manager
    def pinger(self):
        ip = self.ip
        try:
            commandOutput = str(subprocess.check_output('ping -n 1 ' + ip))
        except subprocess.CalledProcessError:  # Log and check router connection
            winsound.PlaySound("!", winsound.SND_ASYNC)  # Audio notifier - no delay
            self.createLogFile(ip)
            return False
        ping = int((re.search('time(\D)(\d+)', commandOutput)).group(2))  # 0 = time, 1 = <|=, 2 = digits
        self.prevPingManager(ping)
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

    # doesn't get used by the "parent" (not actually a parent) but eh, might be useful one day
    def display(self, ip):
        os.system('cls')
        print('PingTester to ' + ip)
        print('Highest ping: %sms' % self.highestPing)
        print('Avg ping: %sms' % self.avgNum)
        for pings in self.prevNums:  # Prints previous pings stored in prevNums
            print(pings, 'ms', sep='')
        print('\n\n\nLast disconnect: %s' % self.lastDisconnect, end='')

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
        print("Disconnection: [%s]" % ip)
        dayAndTime = self.getTime()
        fd = open(dayAndTime.date().__str__() +'.txt', mode='a')
        fd.write('Disconnection occurred @ %s:%s:%s to address %s\n' % (dayAndTime.hour, dayAndTime.minute, dayAndTime.second, ip))
        fd.close()
        self.lastDisconnect = str(dayAndTime.time().hour) + ":" + str(dayAndTime.time().minute) + ":" + str(dayAndTime.time().second)

