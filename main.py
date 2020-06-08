# PepeLeave

"""
V3: Added date support and sound on error. Added default gateway finder instead of typing it in. ---OUTDATED---
V3.1: Added a last disconnect. 
v3.2: Added a one time line that shows the date. Optimized code. Fixed bugs. Added a small debug screen.
v4.0 i feel like i'm dumpster diving...
"""

import routerPinger, subprocess, re, os
import datetime, time

class interface:
    routerAddress = ""

    def __init__(self):
        print("Initializing...")
        self.routerAddress = routerPinger.routerTester().localIP
        self.prevNums = []
        self.lastDisconnect = ":)\n"
        if not os.path.isdir("Logs"):
            print("First time setup")
            os.mkdir('Logs')
        os.chdir('Logs')  # For logging into the Logs subfolder

    def pinger(self, ip):
        commandOutput = str(subprocess.check_output('ping -n 1 ' + ip))
        ping = int((re.search('time(\D)(\d+)', commandOutput)).group(2))  # 0 = time, 1 = <|=, 2 = digits
        self.display(ping, ip)
        return ping, ip

    def display(self, ping, ip):
        prevNums = self.prevNums
        if len(prevNums) <= 10:  # Adds the pings to the list for averaging and printing
            prevNums.append(ping)
        elif len(prevNums) > 10:  # Removes first entry and replaces it with the new one
            del prevNums[0]
            prevNums.append(ping)
        avgNum = int(sum(prevNums) / len(prevNums))
        clear = lambda: os.system('cls')
        clear()
        print('PingTester to ' + ip)
        print('Avg ping: %sms' % avgNum)
        for pings in prevNums:  # Prints previous pings stored in prevNums
            print(pings, 'ms', sep='')
        print('\n\n\nLast disconnect: %s' % self.lastDisconnect, end='')

    def looper(self, ip):
        while True:
            try:
                self.pinger(ip)
            except subprocess.CalledProcessError: # Log and check router connection
                self.createLogFile(ip)
                while True: #pointless to reping google when router is down. keeps checking until router is up
                    try:
                        self.pinger(self.routerAddress)
                        break
                    except subprocess.CalledProcessError:
                        self.createLogFile(self.routerAddress) # router connection failed
                        time.sleep(1)
            time.sleep(1)


    def getTime(self):
        # 24 hr time
        return datetime.datetime.now()

    def createLogFile(self, ip):
        print("Connection Error occured and logged %s" % ip)
        dayAndTime = self.getTime()
        fd = open(dayAndTime.date().__str__() +'.txt', mode='a')
        fd.write('Error occured @ %s:%s:%s to address %s\n' % (dayAndTime.hour, dayAndTime.minute, dayAndTime.second, ip))
        fd.close()
        self.lastDisconnect = str(dayAndTime.time().hour) + ":" + str(dayAndTime.time().minute) + ":" + str(dayAndTime.time().second)


obj = interface()
obj.looper("8.8.8.8")
