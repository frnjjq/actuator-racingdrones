import csv
import math

parameters_name = ("discard", "skip")

def calculate_parameters(latency, jitter, bandwidth, packetloss, current_parameters):
    """ From the network Q4S parameters generats the coder options."""
    #pylint: disable=unused-argument

    if math.isnan(packetloss):
           return current_parameters
    if packetloss > 0:
        with open("rules.csv",encoding="utf-8") as rules_csv:
            reader = csv.reader(rules_csv)
            is_next = False
            for row in reader:
                if is_next:
                    return row
                else:
                    is_next= True 
                    for field, parameter in zip(row, current_parameters):
                        if field != str(parameter):
                            is_next = False
    elif packetloss == 0:
        with open("rules.csv",encoding="utf-8") as rules_csv:
            reader = csv.reader(rules_csv)
            for row in reader:
                is_line= True 
                for field, parameter in zip(row, current_parameters):
                    if field != str(parameter):
                        is_line = False
                if is_line:
                    for element in past_row:
                        if not element.isdigit():
                            return current_parameters
                    return past_row
                past_row = row
    return current_parameters
