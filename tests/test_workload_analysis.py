import unittest
from models.workload_analysis import workload_score

class TestWorkloadAnalysis(unittest.TestCase):
    def test_workload_score(self):
        score = workload_score(10, 40, 2, 5, 8)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0)

if __name__ == "__main__":
    unittest.main()
