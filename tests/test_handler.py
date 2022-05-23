import unittest

from components.dataHandler import dataHandler
from components.loader import Loader


class MyTestCase(unittest.TestCase):
    def test_getTime(self):
        loader = Loader()
        data = loader.importData("../data/mini_json_dataset.json")
        handler = dataHandler()
        handler.getTime(data)

        assert len(handler.times) == 144  # assert that times were saved for each duty

    def test_getBreaks(self):
        loader = Loader()
        data = loader.importData("../data/mini_json_dataset.json")
        handler = dataHandler()
        handler.getBreaks(data)

        assert len(handler.breaks) == 710  # assert that every break is calculated (should be 710 with the example file)
if __name__ == '__main__':
    unittest.main()
