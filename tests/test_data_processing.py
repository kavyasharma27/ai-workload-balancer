import unittest
from utils.data_processing import load_employee_data, validate_employee_data

class TestDataProcessing(unittest.TestCase):
    def test_load_and_validate(self):
        df = load_employee_data("data/employees.json")
        self.assertTrue(validate_employee_data(df))

if __name__ == "__main__":
    unittest.main()
