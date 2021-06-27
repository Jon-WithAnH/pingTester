import subprocess, re

class routerTester:
    # REQS
    '''
    Locate router address
    Grab address
    Check validity
        if not valid
            ask user to verify
    Return router address
    '''

    def __init__(self):
        self.localIP = self.defaultGrabber()

    # Grabs default gateway
    def defaultGrabber(self):
        commandOutput = str(subprocess.check_output('ipconfig'))
        if len(commandOutput) < 60:
            self.informAndKillProcess(commandOutput)
        gatewayAddressLIST = (re.findall('Default Gateway\D+(\d+.\d+.\d+.\d+)', commandOutput))
        if len(gatewayAddressLIST)>1:
            print(">1 network adaptors found. VPN or equivalent might be running.\nRequesting user verification...")
            # I'm not sure how windows will order network adaptors.
            # On my machine, router address is the second match
            localIP=gatewayAddressLIST[1]
            localIP = self.IPVerification(localIP)
        else:
            localIP=gatewayAddressLIST[0]
            if len(localIP) != 11:
                # need more data to see variances in router addresses. Verify until then.
                print("WARNING: Suspicious IP: [%s]" % localIP)
                localIP = self.IPVerification(localIP)
        return localIP

    def informAndKillProcess(self, commandOutput):
        print("ERROR: Unexpected response from command. Please screenshot this window and send to developer. Killing process...")
        print(commandOutput)
        input("Enter to continue...")
        exit(1)

    def IPVerification(self, ip):
        if input("Old Gateway [%s]\nPlease confirm IP. Do you want to change default gateway? (y/n) " % ip).lower() == "y":
            cont = 'n'
            localIP = ip
            while cont == 'n':
                localIP = input("Please enter default gateway: ")
                print("Old Gateway [%s]" % ip)
                print("You entered [%s]" % localIP)
                cont = input("Is this correct? (y/n)").lower()
            return localIP
        return ip
