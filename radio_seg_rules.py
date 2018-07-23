import math

parameters_name = ("skip", )

def calculate_parameters(latency, jitter, bandwidth, packetloss, current_parameters):
    """ From the network Q4S parameters generats the coder options."""
    #pylint: disable=unused-argument
    if math.isnan(packetloss):
        frame_skipping = 0
    elif packetloss == 0:
        frame_skipping = 0
    elif packetloss < 0.05:
        frame_skipping = 2
    elif packetloss < 0.1:
        frame_skipping = 4
    elif packetloss < 0.15:
        frame_skipping = 6
    elif packetloss < 0.2:
        frame_skipping = 8
    elif packetloss < 0.25:
        frame_skipping = 10
    elif packetloss < 0.30:
        frame_skipping = 12
    elif packetloss < 0.35:
        frame_skipping = 14
    elif packetloss < 0.4:
        frame_skipping = 16
    elif packetloss < 0.45:
        frame_skipping = 18
    elif packetloss < 0.5:
        frame_skipping = 20
    else:
        frame_skipping = 25
    return (frame_skipping,  )