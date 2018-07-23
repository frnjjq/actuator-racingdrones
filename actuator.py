#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This module implements the RacingDrones Actuator

This module is intended to be executed as the main. It listen fron Q4S messages
, selects the best quality parameters for the coder and send those to the coder.

"""

import importlib
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
    "    -c,   --coder    String containing the ip and port of\n"
    "                     the coder. The format is 192.168.0.1:8080\n"
    "    -r    --rules    Python file that contains the implementation\n"
    "                     of the rules and parameters to decide\n"     
)


def main(argv):
    """Main function it starts the server"""

    port_number, coder_ip, coder_port, rules_file = parse_arguments(argv)
    rules = importlib.import_module(rules_file, __name__)
    importlib.invalidate_caches()
    try:
        server = socketserver.UDPServer(('', port_number), UDPHandler)
        server.coder_direction = (coder_ip, coder_port)
        server.rules = rules
        print('\033[94m', 'INFO: Started UDP server on port ', port_number, '\033[0m')
        server.serve_forever()
    except KeyboardInterrupt:
        print('\033[94m', 'INFO: ^C received, shutting down UDP server', '\033[0m')
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
        parameters_name = self.server.rules.parameters_name

        latency, jitter, bandwidth, packetloss = parse_metrics(data)
        current_parameters = retrieve_parameters (coder_ip, coder_port, parameters_name)
        parameters = self.server.rules.calculate_parameters(latency, jitter, bandwidth, packetloss, current_parameters)
        result = send_coder_parameters(coder_ip, coder_port, parameters_name, parameters)

        for name, parameter, result in zip(parameters_name, parameters, result):
            if result :
                print('\033[94m',"INFO: Set coder to", name, ":", parameter, '\033[0m')
            else :
                print('\033[93m'"WARN: Failed to set coder to", name, ":", parameter, '\033[0m')
        return


def send_coder_parameters(coder_ip, coder_port, parameters_name, parameters):
    """ Send the parameters given to the Ip and port via HTTP."""

    result = []
    conn = http.client.HTTPConnection(coder_ip, coder_port)
    for name, parameter in zip(parameters_name, parameters):
        try:
            conn.request('POST', '/' + name + '/' + str(parameter))
        except ConnectionRefusedError:
            print('\033[91m',"ERROR: Not listening coder in ", coder_ip, ":", str(coder_port), '\033[0m')
            result.append(False)
            break
        res = conn.getresponse()
        if res.status == 200:
            result.append(True)
        else:
            result.append(False)
    conn.close()
    return result

def retrieve_parameters (coder_ip, coder_port, parameters_name):
    result = []
    conn = http.client.HTTPConnection(coder_ip, coder_port)
    for name in parameters_name:
        try:
            conn.request('GET', '/' + name)
        except ConnectionRefusedError:
            print('\033[91m',"ERROR: Not listening coder in ", coder_ip, ":", str(coder_port), '\033[0m')
            result.append(False)
            break
        res = conn.getresponse()
        result.append(int(res.read()))
    conn.close()
    return result


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
    rules_file = ""
    try:
        optlist, dummy = getopt.getopt(
            argv[1:], "p:c:r:h", ["port=","rules=", "coder=", "help"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for option, value in optlist:
        if option in ("-p", "--port"):
            try:
                port_number = int(value)
            except ValueError:
                print('\033[91m',"ERROR: The port is not a integer", '\033[0m')
                usage()
                sys.exit(2)
        elif option in ("-c", "--coder"):
            value = value.split(":")
            if len(value) != 2:
                print('\033[91m',"ERROR: The coder direction is not ok", len(value), '\033[0m')
                usage()
                sys.exit(2)
            coder_ip = value[0]
            try:
                coder_port = int(value[1])
            except ValueError:
                print('\033[91m',"ERROR: The port of the coder is not a integer", '\033[0m')
                usage()
                sys.exit(2)
        elif option in ("-r", "--rules"):
            rules_file = value

        elif option in ("-h", "--help"):
            usage()
            sys.exit(0)
    if port_number == -1 or coder_ip == "" or coder_port == -1 or rules_file == "":
        print('\033[91m',"ERROR: The required parameters are not supplied", '\033[0m')
        usage()
        sys.exit(2)
    return port_number, coder_ip, coder_port, rules_file


def usage():
    """ Print usage to the terminal"""
    print(USAGE_MESSAGE)
    return


if __name__ == "__main__":

    main(sys.argv)
