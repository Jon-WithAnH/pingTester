## Handle the actual pinging to the IP's and logging ##

import subprocess, re, os
import datetime
import winsound


class interface:

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
        commandOutput = self.sendPingCommendToCMD(ip)
        if not commandOutput:
            return False
        ping = self.ping(ip, commandOutput)
        self.prevPingManager(ping)
        if ping >= self.highPingThreshold: # threshold passed. needs to be logged
            self.logHighPing(ping, ip)
        return ping, ip

    def ping(self, ip, commandOutput):
        try:
            ping = int((re.search('time(\D)(\d+)', commandOutput)).group(2))  # 0 = time, 1 = <|=, 2 = digits
            return ping
        except AttributeError as err:
            # FIXME: some grouping error when valid local connection but failed ping, not sure why, but error's here. unable to replicate
            self.crashLog(ip, commandOutput, err)
            input("ERROR: Possible invalid command response. Check log for details. Enter to continue.")
            raise AttributeError

    def sendPingCommendToCMD(self, ip):
        try:
            commandOutput = str(subprocess.check_output('ping -n 1 ' + ip))
            return commandOutput
        except subprocess.CalledProcessError:  # Log and check router connection
            winsound.PlaySound("!", winsound.SND_ASYNC)  # Audio notifier - no delay
            self.logErrorInfo(ip)
            return False

    # keeps track of previous ping stuff
    def prevPingManager(self, ping):
        self.checkAndMaybeChangeHighestPing(ping)
        # --- List management --- #
        prevNums = self.prevNums
        if len(prevNums) <= self.pingsToDisplay:  # Adds the pings to the list for averaging and printing
            prevNums.append(ping)
        elif len(prevNums) > self.pingsToDisplay:  # Removes first entry and replaces it with the new one
            del prevNums[0]
            prevNums.append(ping)
        self.avgNum = int(sum(prevNums) / len(prevNums))

    def checkAndMaybeChangeHighestPing(self, ping):
        if ping > self.highestPing:
            self.highestPing = ping

    # depreciated. kept for future records
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

    def logHighPing(self, ping, ip):
        dayAndTime = self.getTime()
        fd = open(dayAndTime.date().__str__() +'.txt', mode='a')
        fd.write('WARNING: high ping of [%s] occurred @ %s:%s:%s to address %s\n' %
                 (ping, dayAndTime.hour, dayAndTime.minute, dayAndTime.second, ip))
        fd.close()

    def logErrorInfo(self, ip):
        print("Disconnection: [%s]" % ip)
        dayAndTime = self.getTime()
        fd = open(dayAndTime.date().__str__() +'.txt', mode='a')
        fd.write('Disconnection occurred @ %s:%s:%s to address %s\n' % (dayAndTime.hour, dayAndTime.minute, dayAndTime.second, ip))
        fd.close()
        self.lastDisconnect = str(dayAndTime.time().hour) + ":" + str(dayAndTime.time().minute) + ":" + str(dayAndTime.time().second)

    def crashLog(self, ip, commandStr, err):
        print("Disconnection: [%s]" % ip)
        dayAndTime = self.getTime()
        fd = open('Crash.txt', mode='a')
        fd.write('PingTester.py crash @ %s:%s:%s to address %s\n' % (dayAndTime.hour, dayAndTime.minute, dayAndTime.second, ip))
        fd.write('commandOutput [%s]\n' % commandStr)
        fd.write('msg: [%s]\n' % err)
        fd.close()


