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
Example:
    python actuator.py -p 3001 -c 127.0.0.1:3000
```
## License
Apache License 2.0. See LICENSE file in the root.

