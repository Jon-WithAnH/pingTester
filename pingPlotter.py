import matplotlib.pyplot as plt
import random
import configReader, pingTester, gatewayGrabber

class Graph():

    def __init__(self):
        self.pingstoDisplay = int(configInterface.pingsToDisplay)
        self.xaxis = []
        self.test = []
        self.highestPing = 0
        ## generate x-labels in range provided by config

    def startUp(self):
        for x in range(self.pingstoDisplay):
            self.xaxis.append(x+1)
            self.test.append(OUTBOUND_IP_TO_PING.pinger())
            self.showGraph()
            plt.pause(.1)

    def showGraph(self):
        if self.test[-1] > self.highestPing: self.highestPing = self.test[-1]
        title = f'Current ping: {self.test[-1]}\nMax Ping: {self.highestPing}'
        plt.clf()
        plt.axis((1, self.pingstoDisplay, 0, 150))
        plt.plot(self.xaxis, self.test, label=OUTBOUND_IP_TO_PING.ip, marker="o")
        plt.legend()
        plt.grid()
        plt.title(title)
        plt.ylabel("Ping (in ms)")

    def updateLoop(self):
        self.startUp()
        test = self.test
        while True:
            del test[0]
            self.test.append(OUTBOUND_IP_TO_PING.pinger())
            self.showGraph()
            plt.gcf().canvas.draw_idle()
            plt.gcf().canvas.start_event_loop(1)


# read info from config file
configInterface = configReader.configInterface()
configInterface.readConfig()

OUTBOUND_IP_TO_PING = pingTester.interface(configInterface.defaultIP, int(configInterface.pingsToDisplay), int(configInterface.highPingThreshold))
LOCAL_IP_TO_PING = pingTester.interface(gatewayGrabber.routerTester().localIP, configInterface.pingsToDisplay, 20)
obj = Graph()
obj.updateLoop()
