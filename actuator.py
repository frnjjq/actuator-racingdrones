#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This module implements the RacingDrones Actuator

This module is intended to be executed as the main. It listen fron Q4S messages
, selects the best quality parameters for the coder and send those to the coder.

"""

import socketserver
import http.client
import math
import sys
import getopt

USAGE_MESSAGE = (
    "\n"
    "Usage:   python3 actuator.py [OPTIONS] \n"
    "\n"
    "Racingdrones Q4S coder actuator\n"
    "\n"
    "Options:\n"
    "    -h,   --help     Show help\n"
    "    -p,   --port     Specify the UDP port to listen for Q4S\n"
    "                     messages\n"
    "    -c,   --coder   String containing the ip and port of\n"
    "                     the coder. The format is 192.168.0.1:8080\n"
)


def main(argv):
    """Main function it starts the server"""

    port_number, coder_ip, coder_port = parse_arguments(argv)

    try:
        server = socketserver.UDPServer(('', port_number), UDPHandler)
        server.coder_direction = (coder_ip, coder_port)
        print('INFO: Started UDP server on port ', port_number)
        server.serve_forever()
    except KeyboardInterrupt:
        print('INFO: ^C received, shutting down UDP server')
        server.shutdown()
    return


class UDPHandler(socketserver.BaseRequestHandler):
    """Handler class for the UDP server"""

    def handle(self):
        """
        Process the UDP packet extracting the parameters. It sends the http
        requests when all the parameters has benn sent.
        """

        data = self.request[0].strip()
        data = data.decode("utf-8")
        coder_ip = self.server.coder_direction[0]
        coder_port = self.server.coder_direction[1]

        latency, jitter, bandwidth, packetloss = parse_metrics(data)
        discard_level, frame_skipping = calculate_parameters(
            latency, jitter, bandwidth, packetloss)
        if send_coder_parameters(coder_ip, coder_port, discard_level, frame_skipping):
            print("INFO: Set coder to discard: ", discard_level, " skip: ", frame_skipping)

        return


def send_coder_parameters(coder_ip, coder_port, discard_level, frame_skipping):
    """ Send the parameters given to the Ip and port via HTTP."""

    conn = http.client.HTTPConnection(coder_ip, coder_port)
    try:
        conn.request('POST', '/discard/' + str(discard_level))
    except ConnectionRefusedError:
        print("ERROR: Not listening coder in ", coder_ip, ":", str(coder_port))
        conn.close()
        return False
    res = conn.getresponse()
    status_1 = res.status

    try:
        conn.request('POST', '/skip/' + str(frame_skipping))
    except ConnectionRefusedError:
        print("ERROR: Not listening coder in ", coder_ip, ":", str(coder_port))
        conn.close()
        return False
    res = conn.getresponse()
    status_2 = res.status

    conn.close()
    return status_1 == 200 and status_2 == 200


def calculate_parameters(latency, jitter, bandwidth, packetloss):
    """ From the network Q4S parameters generats the coder options."""
    #pylint: disable=unused-argument
    if math.isnan(bandwidth):
        discard_level = 3
        frame_skipping = 0
    elif bandwidth > 6192:
        discard_level = 0
        frame_skipping = 0
    elif bandwidth > 6000:
        discard_level = 1
        frame_skipping = 0
    elif bandwidth > 5800:
        discard_level = 2
        frame_skipping = 0
    elif bandwidth > 5600:
        discard_level = 3
        frame_skipping = 0
    elif bandwidth > 5400:
        discard_level = 4
        frame_skipping = 0
    elif bandwidth > 4000:
        discard_level = 5
        frame_skipping = 0
    else:
        discard_level = 5
        frame_skipping = int(30 - (bandwidth/4000)*30)
    return discard_level, frame_skipping


def parse_metrics(text):
    """ Parses the Q4S message into the corresponding metrics"""
    latency = float('nan')
    jitter = float('nan')
    bandwidth = float('nan')
    packetloss = float('nan')

    text = text.split()
    for index, word in enumerate(text[:-1]):
        if word == "Latency:":
            try:
                latency = float(text[index+1])
            except ValueError:
                latency = float('nan')
        elif word == "Jitter:":
            try:
                jitter = float(text[index+1])
            except ValueError:
                jitter = float('nan')
        elif word == "PacketLoss:":
            try:
                packetloss = float(text[index+1])
            except ValueError:
                packetloss = float('nan')
        elif word == "BandWidth:":
            try:
                bandwidth = float(text[index+1])
            except ValueError:
                bandwidth = float('nan')
    return latency, jitter, bandwidth, packetloss


def parse_arguments(argv):
    """ Parses the program arguments in order to ensure that everthing is alright"""

    port_number = -1
    coder_ip = ""
    coder_port = -1
    try:
        optlist, dummy = getopt.getopt(
            argv[1:], "p:c:h", ["port=", "coder=", "help"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for option, value in optlist:
        if option in ("-p", "--port"):
            try:
                port_number = int(value)
            except ValueError:
                print("ERROR: The port is not a integer")
                usage()
                sys.exit(2)
        elif option in ("-c", "--coder"):
            value = value.split(":")
            if len(value) != 2:
                print("ERROR: The coder direction is not ok", len(value))
                usage()
                sys.exit(2)
            coder_ip = value[0]
            try:
                coder_port = int(value[1])
            except ValueError:
                print("ERROR: The port of the coder is not a integer")
                usage()
                sys.exit(2)
        elif option in ("-h", "--help"):
            usage()
            sys.exit(0)
    if port_number == -1 or coder_ip == "" or coder_port == -1:
        print("ERROR: The required parameters are not supplied")
        usage()
        sys.exit(2)
    return port_number, coder_ip, coder_port


def usage():
    """ Print usage to the terminal"""
    print(USAGE_MESSAGE)
    return


if __name__ == "__main__":

    main(sys.argv)
