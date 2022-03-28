import subprocess, re


class RouterTester:
    '''
    Class to handle grabbing IP to router.
    '''

    def __init__(self):
        self.localIP = self.default_grabber()

    # Grabs default gateway
    def default_grabber(self):
        commandOutput = str(subprocess.check_output('ipconfig'))
        if len(commandOutput) < 60:
            self._informAndKillProcess(commandOutput)
        gatewayAddressLIST = (re.findall('Default Gateway\D+(\d+.\d+.\d+.\d+)', commandOutput))
        if len(gatewayAddressLIST)>1:
            print(">1 network adaptors found. VPN or equivalent might be running.\nRequesting user verification...")
            # I'm not sure how windows will order network adaptors.
            # On my machine, router address is the second match
            localIP = gatewayAddressLIST[1]
            localIP = self._IPVerification(localIP)
        else:
            localIP = gatewayAddressLIST[0]
            if len(localIP) != 11:
                # need more data to see variances in router addresses. Verify until then.
                print("WARNING: Suspicious IP: [%s]" % localIP)
                localIP = self._IPVerification(localIP)
        return localIP

    def _informAndKillProcess(self, commandOutput):
        print("ERROR: Unexpected response from command. Please screenshot this window and send to developer. Killing process...")
        print(commandOutput)
        input("Enter to continue...")
        exit(1)

    def _IPVerification(self, ip):
        if input("Old Gateway [%s]\nPlease confirm IP. Is this the IP you want to use? (y/n) " % ip).lower() == "n":
            cont = 'n'
            localIP = ip
            while cont == 'n':
                localIP = input("Please enter default gateway: ")
                print("Old Gateway [%s]" % ip)
                print("You entered [%s]" % localIP)
                cont = input("Is this correct? (y/n) ").lower()
            return localIP
        return ip
