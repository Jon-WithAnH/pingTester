import subprocess, os, signal
import re

class routerTester:
    # REQS
    '''
    ping google, log if connection drops
    if connection drops, ping router, if router is successful, log router success and ping google again, logging if failed

    do i want to reping each failure or just the once?

    record connection drops

    '''
    localIP = ""

    def __init__(self):
        self.localIP = self.defaultGrabber()

    def defaultGrabber(self):
        print("Grabbing IP...")
        commandOutput = str(subprocess.check_output('ipconfig'))
        if len(commandOutput) < 60:
            print("ERROR 339: Initial connection to router failed. Please contact Dev. Killing process...")
            input("Enter to continue")
        localIP = (re.search('Default Gateway(\D+)(\S+)', commandOutput)).group(2)
        localIP = localIP[0:-5] # removes \r\n at end of line. eg 192.168.0.1\r\n
        if len(localIP) > 11:
            print("WARNING: Suspicious IP: [%s]" % localIP)
        else:
            print('IP grabbed: [%s] ' % localIP)
        self.localIP = localIP
        return self.localIP
