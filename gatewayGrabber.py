import subprocess, re

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
        # WARNING: only works if ip has 3 dots eg 192.14.1 would not work. 192.168.11.22.3 would not work
        localIP = (re.search('Default Gateway(\D+)(\d+.\d+.\d+.\d+)', commandOutput)).group(2)
        if len(localIP) > 11:
            print("WARNING: Suspicious IP: [%s]" % localIP)
            input("Please confirm IP and press enter to continue...")
        self.localIP = localIP
        return self.localIP
