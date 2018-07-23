import math

parameters_name = ("discard","skip")

def calculate_parameters(latency, jitter, bandwidth, packetloss, current_parameters):
    #pylint: disable=unused-argument

    print ("latency", latency)
    print ("jitter", jitter)
    print ("bandwidth", bandwidth)
    print ("packetloss", packetloss)
    print ("current_parameters", current_parameters)
    return (0,0)