
import argparse

from pythonosc import osc_message_builder
from pythonosc import udp_client

ZYNADD_URI = "127.0.0.1"
ZYNADD_PORT = 6666

class ZynAddSubFxOscControl:

    def __init__(self):

        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default=ZYNADD_URI,
                    help="The ip of the OSC server")
        parser.add_argument("--port", type=int, default=ZYNADD_PORT,
                    help="The port the OSC server is listening on")
        args = parser.parse_args()

        self.client = udp_client.SimpleUDPClient(args.ip, args.port)

    def loadPart(self, part, xiz):
        self.client.send_message("/load-part", [part, xiz])
