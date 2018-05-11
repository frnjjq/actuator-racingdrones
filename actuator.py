#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import http.client
import sys
import getopt


def main(argv):

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

    def handle(self):
        data = self.request[0].strip()
        coder_ip = self.server.coder_direction[0]
        coder_port = self.server.coder_direction[1]

        latency, jitter, bandwidth, packetloss = parse_metrics(data)
        discard_level, frame_skipping = calculate_parameters(
            latency, jitter, bandwidth, packetloss)
        send_coder_parameters(coder_ip, coder_port,
                              discard_level, frame_skipping)

        return


def send_coder_parameters(ip, port, discard_level, frame_skipping):
    conn = http.client.HTTPConnection(ip, port)

    conn.request('POST', '/discard/' + discard_level)
    res = conn.getresponse()
    while not res.closed:
        res.read()
    if res.status != 200:
        conn.close()
        return

    conn.request('POST', '/skip/' + frame_skipping)
    res = conn.getresponse()
    while not res.closed:
        res.read()
    if res.status != 200:
        conn.close()
        return
    conn.close()
    return


def calculate_parameters(latency, jitter, bandwidth, packetloss):
    discard_level = 3
    frame_skipping = 0
    return discard_level, frame_skipping


def parse_metrics(text):
    latency = float('nan')
    jitter = float('nan')
    bandwidth = float('nan')
    packetloss = float('nan')

    text.split()
    text = iter(text)
    for word in text:
        if word == "Latency:":
            latency = float(text.next())
        elif word == "Jitter:":
            jitter = float(text.next())
        elif word == "PacketLoss:":
            bandwidth = float(text.next())
        elif word == "BandWidth:":
            packetloss = float(text.next())
    return latency, jitter, bandwidth, packetloss


def parse_arguments(argv):

    port_number = -1
    coder_ip = ""
    coder_port = -1
    try:
        optlist, arglist = getopt.getopt(
            argv[1:], "p:c:h", ["port=", "coder=", "help"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for o, a in optlist:
        if o in ("-p", "--port"):
            port_number = int(a)
        elif o in ("-c", "--coder"):
            a = a.split(":")
            if len(a) is not 2:
                print("ERROR: The coder direction is not ok", len(a))
                usage()
                sys.exit(2)
            coder_ip = a[0]
            coder_port = int(a[1])
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
    if port_number is -1 or coder_ip is "" or coder_port is -1:
        print("ERROR: The required parameters are not supplied")
        usage()
        sys.exit(2)
    return port_number, coder_ip, coder_port


def usage():
    message = (
        "\n"
        "Usage:   python3 actuator.py [OPTIONS] \n"
        "\n"
        "Racingdrones Q4S coder actuator\n"
        "\n"
        "Options:\n"
        "    -h,   --help     Show help\n"
        "    -p,   --port     Specify the UDP port to listen for Q4S\n"
        "                     messages\n"
        "    -o,   --output   String containing the ip and port of\n"
        "                     the coder. The format is 192.168.0.1:8080\n"
    )
    print(message)
    return


if __name__ == "__main__":
    main(sys.argv)
