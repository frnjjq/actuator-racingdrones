import math

parameters_name = ("discard",)
def calculate_parameters(latency, jitter, bandwidth, packetloss, current_parameters):
    """ From the network Q4S parameters generats the coder options."""
    #pylint: disable=unused-argument

    if math.isnan(bandwidth):
        discard_level = 3
    elif bandwidth > 9650:
        discard_level = 0
    elif bandwidth > 9600:
        discard_level = 1
    elif bandwidth > 9400:
        discard_level = 2
    elif bandwidth > 8500:
        discard_level = 3
    elif bandwidth > 7000:
        discard_level = 4
    elif bandwidth > 5000:
        discard_level = 5
    else:
        discard_level = 5

    return (discard_level, )