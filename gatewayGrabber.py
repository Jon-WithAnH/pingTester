import subprocess, re

class routerTester:
    # REQS
    '''
    ping google, log if connection drops
    if connection drops, ping router, if router is successful, log router success and ping google again, logging if failed

    do i want to reping each failure or just the once?

    record connection drops

    '''

    def __init__(self):
        self.localIP = self.defaultGrabber()

    # Grabs default gateway
    def defaultGrabber(self):
        commandOutput = str(subprocess.check_output('ipconfig'))
        if len(commandOutput) < 60:
            print("ERROR: Unexpected response from command. Please contact Dev. Killing process...")
            input("Enter to continue")
        # WARNING: only works if ip has 3 dots eg 192.14.1 would not work. 192.168.11.22.3 would not work
        # more than 4 dots will be cautch but if statement
        localIP = (re.search('Default Gateway(\D+)(\d+.\d+.\d+.\d+)', commandOutput)).group(2)
        if len(localIP) > 11:
            print("WARNING: Suspicious IP: [%s]" % localIP)
            localIP = self.manualEnter(localIP)
        return localIP

    def manualEnter(self, ip):
        if input("Please confirm IP. Do you want to change default gateway? (y/n)").lower() == "y":
            cont = 'n'
            localIP = ip
            while cont == 'n':
                localIP = input("Please enter default gateway: ")
                print("Old Gateway [%s]" % ip)
                print("You entered [%s]" % localIP)
                cont = input("Is this correct? (y/n)").lower()
            return localIP
        return ip
