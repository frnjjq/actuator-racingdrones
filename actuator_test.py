import unittest
import math
from actuator import parse_metrics,calculate_parameters

class TestParseMetrics(unittest.TestCase):

    def test_latency(self):
        message  = "nothing Latency: 89.359874523 nothing nothing"
        latency, jitter, bandwidth, packetloss = parse_metrics(message)
        self.assertEqual(latency, 89.359874523)
        self.assertTrue(math.isnan(jitter))
        self.assertTrue(math.isnan(bandwidth))
        self.assertTrue(math.isnan(packetloss))

    def test_jitter(self):
        message  = "nothing Jitter: 89.359874523 nothing nothing"
        latency, jitter, bandwidth, packetloss = parse_metrics(message)
        self.assertTrue(math.isnan(latency))
        self.assertEqual(jitter, 89.359874523)
        self.assertTrue(math.isnan(bandwidth))
        self.assertTrue(math.isnan(packetloss))

    def test_bandwidth(self):
        message  = "nothing BandWidth: 89.359874523 nothing nothing"
        latency, jitter, bandwidth, packetloss = parse_metrics(message)
        self.assertTrue(math.isnan(latency))
        self.assertTrue(math.isnan(jitter))
        self.assertEqual(bandwidth, 89.359874523)
        self.assertTrue(math.isnan(packetloss))

    def test_packetloss(self):
        message  = "nothing PacketLoss: 89.359874523 nothing nothing"
        latency, jitter, bandwidth, packetloss = parse_metrics(message)
        self.assertTrue(math.isnan(latency))
        self.assertTrue(math.isnan(jitter))
        self.assertTrue(math.isnan(bandwidth))
        self.assertEqual(packetloss, 89.359874523)
        
    def test_couple(self):
        message  = "nothing PacketLoss: 89.359874523 nothing nothing Jitter: 24.011993 nothing nothing"
        latency, jitter, bandwidth, packetloss = parse_metrics(message)
        self.assertTrue(math.isnan(latency))
        self.assertEqual(jitter, 24.011993)
        self.assertTrue(math.isnan(bandwidth))
        self.assertEqual(packetloss, 89.359874523)

if __name__ == '__main__':
    unittest.main()