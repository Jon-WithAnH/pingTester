import pingTester, gatewayGrabber
import time, os
import configReader

class combineTwoIPAddresses():
    def __init__(self, outbound, router):
        self.outbound = outbound
        self.local = router
        self.start()

    def start(self):
        while len(self.outbound.prevNums) < self.outbound.pingsToDisplay+1:
            # rapidly ping addresses until amount [pingsToDisplay] is shown
            self.quicklyPingAddresses()
        while True:
            time.sleep(1)
            if not self.outbound.pinger():
                # outbound ping failed
                while not self.local.pinger():
                    # router is down
                    print("Connection to router failed. Time between router pings is 4 seconds. Please check connection")
                    time.sleep(4)
            self.display()

    def quicklyPingAddresses(self):
        self.outbound.pinger()
        self.local.pinger()
        self.display()
        time.sleep(.5)

    def pingBothAddresses(self):
        pass

    def display(self):
        spacesToSeperateBy = 50
        os.system('cls')
        print(('PingTester to ' + self.outbound.ip).ljust(spacesToSeperateBy) + "PingTester to " + self.local.ip)
        print(('Highest ping: %sms' % self.outbound.highestPing).ljust(spacesToSeperateBy) + "Highest ping: %sms" % self.local.highestPing)
        print(('Avg ping: %sms' % self.outbound.avgNum).ljust(spacesToSeperateBy) + "Avg ping: %sms" % self.local.avgNum)
        # if outbound succeeds but router fails, there will be an IndexOutOfBound <-- probably not. tested. be aware anyways
        if len(self.outbound.prevNums) <= len(self.local.prevNums):
            for pings in range(len(self.outbound.prevNums)):
                print(("%sms" % self.outbound.prevNums[pings]).ljust(spacesToSeperateBy) + "%sms" % self.local.prevNums[pings])
        print('\n\n\nLast disconnect: %s' % self.outbound.lastDisconnect, end='')


configInterface = configReader.configInterface()
# generate config file is it doesn't already exist
if not os.path.exists('config.txt'):
    print("fnf\n\n")
    time.sleep(1)
    configInterface.createConfig()

# read info from config file
configInterface.readConfig()

OUTBOUND_IP_TO_PING = pingTester.interface(configInterface.defaultIP, int(configInterface.pingsToDisplay), int(configInterface.highPingThreshold))
LOCAL_IP_TO_PING = pingTester.interface(gatewayGrabber.routerTester().localIP, configInterface.pingsToDisplay, 20)

if not os.path.isdir("Logs"):
    os.mkdir('Logs')
os.chdir('Logs')  # For logging into the Logs subfolder

combineTwoIPAddresses(OUTBOUND_IP_TO_PING, LOCAL_IP_TO_PING)
