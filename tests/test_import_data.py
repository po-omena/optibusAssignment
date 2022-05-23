import unittest
from components.loader import Loader




class MyTestCase(unittest.TestCase):
    def test_load_data(self):
        loader = Loader()
        data = loader.importData("../data/mini_json_dataset.json")  # Do NOT change this path

        assert data is not None  # Check if object exists
        assert len(data) == 4  # Check if every json dict was loaded
        assert len(data.get('stops')) == 76  # check if stops was fully loaded
        assert len(data.get('trips')) == 1749  # check if trips was fully loaded
        assert len(data.get('vehicles')) == 97  # check if vehicles was fully loaded
        assert len(data.get('duties')) == 144  # check if duties was fully loaded

if __name__ == '__main__':
    unittest.main()
