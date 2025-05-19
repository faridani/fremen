import unittest
from agentstudio.step_extractor import StepExtractor

class TestStepExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = StepExtractor()

    def test_parse_steps(self):
        text = """1- open chrome\n2- browse to chase.com\n3- login"""
        steps = self.extractor.parse_steps(text)
        self.assertEqual(steps, [
            "open chrome",
            "browse to chase.com",
            "login",
        ])

if __name__ == "__main__":
    unittest.main()
