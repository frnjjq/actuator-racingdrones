import csv
import math

parameters_name = ("discard", "skip")

def calculate_parameters(latency, jitter, bandwidth, packetloss, current_parameters):
    """ From the network Q4S parameters generats the coder options."""
    #pylint: disable=unused-argument
    
    is_next = False
    if not math.isnan(packetloss) and packetloss > 0:
        with open("rules.csv",encoding="utf-8") as rules_csv:
            reader = csv.reader(rules_csv)
            for row in reader:
                if is_next:
                    return row
                else:
                    is_next= True 
                    for field, parameter in zip(row, current_parameters):
                        if field != parameter:
                            is_next = False  
    return current_parameters
