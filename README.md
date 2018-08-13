# actuator-racingdrones
[![Build Status](https://travis-ci.org/frnjjq/actuator-racingdrones.svg?branch=master)](https://travis-ci.org/frnjjq/actuator-racingdrones)  [![Coverage Status](https://coveralls.io/repos/github/frnjjq/actuator-racingdrones/badge.svg)](https://coveralls.io/github/frnjjq/actuator-racingdrones)

Python executable in charge of making decisions about the video coding given Q4S reports from the server.

## Depedencies
* Python 3. Minimum Python version v3.3

## Usage
```
Usage:   python actuator.py [OPTIONS]

Options:
    -h,   --help     Show help
    -p,   --port     Specify the UDP port to listen for Q4S messages
    -c,   --coder    String containing the ip and port ofthe coder. The format is 192.168.0.1:8080
    -r    --rules    Python file that contains the implementation of the rules to decide
Example:
    python actuator.py -p 3001 -c 127.0.0.1:3000 -r csv_rules
```


## Rules Files
For each launch of the actuator a rules file must be supplied to the command line. This rules file adds flexibility to the actuator so new parametes and rules can be handly included. Anyway the default rules for the project are the ones contained in csv_rules.

The rules file define how many parameters are to be managed at the coder. The function that defines the behaviour of those parameters supplied must be implemented too.

The rule files is a Python source file containing two elements. The first one is the parameters_name tuple. This tuple contains a detemined number of strings which name the endpoint on the API of the coder. For Example:
```
parameters_name = ("discard", "skip")

```

This tuple defines that there is only a two parameters to tweak at the coder. The endpoint of the first parameter at the coder  is /discard/**value**. And the second endpoint for the parameters is /skip/**value**.

The second element that must be implemented in the rules file is the function calculate_parameters. This function is in charge of translate the standard Q4S attributes latency, jitter, bandwidth, packetloss to the parameters that are supplied in the variable parameters_name. 

This function takes four attributes(The listed Q4S attributes) and returns a tuple with the same lenght as the parameters_name tuple. Those attributes are floats containing the values found in the Q4S message. Some or all of them can be nan meaning that that parameter was not contained in the Q4S message.

The return number must be a list integer type. For example, for the previous parameters_name.:
```
def calculate_parameters(latency, jitter, bandwidth, packetloss, current_parameters):
    if bandwidth > 9650:
        discard_level = 0
        skip = 3
    else:
        discard_level = 5
        skip = 2
    return discard_level, skip
```

## License
Apache License 2.0. See LICENSE file in the root.

