import unittest
import io
import sys
import math
from actuator import parse_metrics, calculate_parameters, parse_arguments, USAGE_MESSAGE, usage


class TestActuator(unittest.TestCase):

    def test_parse_metrics_latency(self):
        message = "nothing Latency: 89.359874523 nothing nothing"
        latency, jitter, bandwidth, packetloss = parse_metrics(message)
        self.assertEqual(latency, 89.359874523)
        self.assertTrue(math.isnan(jitter))
        self.assertTrue(math.isnan(bandwidth))
        self.assertTrue(math.isnan(packetloss))

    def test_parse_metrics_jitter(self):
        message = "nothing Jitter: 89.359874523 nothing nothing"
        latency, jitter, bandwidth, packetloss = parse_metrics(message)
        self.assertTrue(math.isnan(latency))
        self.assertEqual(jitter, 89.359874523)
        self.assertTrue(math.isnan(bandwidth))
        self.assertTrue(math.isnan(packetloss))

    def test_parse_metrics_bandwidth(self):
        message = "nothing BandWidth: 89.359874523 nothing nothing"
        latency, jitter, bandwidth, packetloss = parse_metrics(message)
        self.assertTrue(math.isnan(latency))
        self.assertTrue(math.isnan(jitter))
        self.assertEqual(bandwidth, 89.359874523)
        self.assertTrue(math.isnan(packetloss))

    def test_parse_metrics_packetloss(self):
        message = "nothing PacketLoss: 89.359874523 nothing nothing"
        latency, jitter, bandwidth, packetloss = parse_metrics(message)
        self.assertTrue(math.isnan(latency))
        self.assertTrue(math.isnan(jitter))
        self.assertTrue(math.isnan(bandwidth))
        self.assertEqual(packetloss, 89.359874523)

    def test_parse_metrics_couple(self):
        message = "nothing PacketLoss: 89.359874523 nothing nothing Jitter: 24.011993 nothing nothing"
        latency, jitter, bandwidth, packetloss = parse_metrics(message)
        self.assertTrue(math.isnan(latency))
        self.assertEqual(jitter, 24.011993)
        self.assertTrue(math.isnan(bandwidth))
        self.assertEqual(packetloss, 89.359874523)

    def test_parse_metrics_no_one(self):
        message = "nothing nothing nothing nothing nothing nothing nothing nothing"
        latency, jitter, bandwidth, packetloss = parse_metrics(message)
        self.assertTrue(math.isnan(latency))
        self.assertTrue(math.isnan(jitter))
        self.assertTrue(math.isnan(bandwidth))
        self.assertTrue(math.isnan(packetloss))

    def test_parse_metrics_wrong(self):
        message = "nothing Jitter: nothing PacketLoss: nothing Latency: nothing BandWidth: nothing nothing"
        latency, jitter, bandwidth, packetloss = parse_metrics(message)
        self.assertTrue(math.isnan(latency))
        self.assertTrue(math.isnan(jitter))
        self.assertTrue(math.isnan(bandwidth))
        self.assertTrue(math.isnan(packetloss))

    def test_parse_arguments_normal(self):
        argv = "exename -p 3000 -c 127.0.0.1:3001".split()
        port_number, coder_ip, coder_port = parse_arguments(argv)
        self.assertEqual(port_number, 3000)
        self.assertEqual(coder_ip, "127.0.0.1")
        self.assertEqual(coder_port, 3001)

        argv = "exename --port 3000 --coder 127.0.0.1:3001".split()
        port_number, coder_ip, coder_port = parse_arguments(argv)
        self.assertEqual(port_number, 3000)
        self.assertEqual(coder_ip, "127.0.0.1")
        self.assertEqual(coder_port, 3001)

    def test_parse_arguments_missing(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        argv = "exename -p 3000".split()
        with self.assertRaises(SystemExit) as cm:
            port_number, coder_ip, coder_port = parse_arguments(argv)

        sys.stdout = sys.__stdout__
        stdout_msg = capturedOutput.getvalue()
        self.assertEqual(cm.exception.code, 2)
        self.assertIn(USAGE_MESSAGE, stdout_msg)

    def test_parse_arguments_extra(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        argv = "exename -p 3000 -c 127.0.0.1:3001 -o".split()
        with self.assertRaises(SystemExit) as cm:
            port_number, coder_ip, coder_port = parse_arguments(argv)

        sys.stdout = sys.__stdout__
        stdout_msg = capturedOutput.getvalue()
        self.assertEqual(cm.exception.code, 2)
        self.assertIn(USAGE_MESSAGE, stdout_msg)

    def test_parse_arguments_help(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        argv = "exename -h".split()
        with self.assertRaises(SystemExit) as cm:
            port_number, coder_ip, coder_port = parse_arguments(argv)

        sys.stdout = sys.__stdout__
        stdout_msg = capturedOutput.getvalue()
        self.assertEqual(cm.exception.code, 0)
        self.assertIn(USAGE_MESSAGE, stdout_msg)

    def test_parse_arguments_wrong_port(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        argv = "exename -p notinteger -c 127.0.0.1:3001".split()
        with self.assertRaises(SystemExit) as cm:
            port_number, coder_ip, coder_port = parse_arguments(argv)

        sys.stdout = sys.__stdout__
        stdout_msg = capturedOutput.getvalue()
        self.assertEqual(cm.exception.code, 2)
        self.assertIn(USAGE_MESSAGE, stdout_msg)

    def test_parse_arguments_wrong_port_ip(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        argv = "exename -p 3000 -c 127.0.0.1:notshit".split()
        with self.assertRaises(SystemExit) as cm:
            port_number, coder_ip, coder_port = parse_arguments(argv)

        sys.stdout = sys.__stdout__
        stdout_msg = capturedOutput.getvalue()
        self.assertEqual(cm.exception.code, 2)
        self.assertIn(USAGE_MESSAGE, stdout_msg)

    def test_parse_arguments_wrong_ip(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        argv = "exename -p 3000 -c wrongip".split()
        with self.assertRaises(SystemExit) as cm:
            port_number, coder_ip, coder_port = parse_arguments(argv)

        sys.stdout = sys.__stdout__
        stdout_msg = capturedOutput.getvalue()
        self.assertEqual(cm.exception.code, 2)
        self.assertIn(USAGE_MESSAGE, stdout_msg)

    def test_usage(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        usage()
        sys.stdout = sys.__stdout__
        stdout_msg = capturedOutput.getvalue()
        self.assertIn(USAGE_MESSAGE, stdout_msg)

    def test_coder_parameters(self):
        return


if __name__ == '__main__':
    unittest.main()
