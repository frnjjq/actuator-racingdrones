#!/usr/bin/python
# -*- coding: utf-8 -*-

import http.server
import http.client
import sys

PORT_NUMBER = 3001
CODER_IP = '192.168.1.36'
CODER_PORT = 3000

def main(argv):
    try:
        server_address = ('', PORT_NUMBER)
        server = HTTPServer(server_address, myHandler)
        print 'Started http server on port ' , PORT_NUMBER
        server.serve_forever()
    except KeyboardInterrupt:
	    print '^C received, shutting down the web server'
	    server.socket.close()

class myHandler(BaseHTTPRequestHandler):

	def do_POST(self):
        #Parsear el mensaje para obtener 

        parameters = calculate_parameters(latency, jitter, bandwidth, packetloss)
        if send_coder_parameters(parameters) is not 0:
            #mandar un error de vuelta
        else
            #mandar un todo Ok de vuelta
        return
  
def send_coder_parameters(discard_level, frame_skipping)
    conn = http.client.HTTPConnection(CODER_IP, CODER_PORT)
    
    conn.request('POST', '/discard/'+ discard_level)
    res = conn.getresponse()
    while not res.closed:
        res.read()
    if response.status != 200:
        conn.close()
        return -1

    conn.request('POST', '/skip/'+ frame_skipping)
    res = conn.getresponse()
    while not res.closed:
        res.read()
    if response.status != 200:
        conn.close()
        return -1
    conn.close()
    return 0

def calculate_parameters(latency, jitter, bandwidth, packetloss)
    if bandwidth > 40000:
        return tuple(2, 3)
    else if 
        return tuple(4, 12)

if __name__ == "__main__":
    main(sys.argv)
