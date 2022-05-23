import os
import unittest

from components.dataHandler import dataHandler
from components.loader import Loader
from components.reports import Reports


class MyTestCase(unittest.TestCase):
    def test_time_report(self):
        if os.path.exists("../reports/timeReport.csv"):  # Check if there is a report file in the reports folder,
            os.remove("../reports/timeReport.csv")  # if there is one, delete it.

        loader = Loader()  # Create object to load data from json
        data = loader.importData("../data/mini_json_dataset.json")  # Get data
        handler = dataHandler()  # Create object to handle data
        handler.getTime(data)  # Get duty times
        Reports.generateTimeReport(handler, "../reports")

        assert os.path.exists("../reports/timeReport.csv")  # Check if report was created

    def test_break_report(self):
        if os.path.exists("../reports/breakReport.csv"):  # Check if there is a report file in the reports folder,
            os.remove("../reports/breakReport.csv")  # if there is one, delete it.

        loader = Loader()  # Create object to load data from json
        data = loader.importData("../data/mini_json_dataset.json")  # Get data
        handler = dataHandler()  # Create object to handle data
        handler.getBreaks(data)  # Get duty times
        Reports.generateBreakReport(handler, "../reports")

        assert os.path.exists("../reports/breakReport.csv")  # Check if report was created

    def test_full_report(self):
        if os.path.exists("../reports/fullReport.csv"):  # Check if there is a report file in the reports folder,
            os.remove("../reports/fullReport.csv")  # if there is one, delete it.

        loader = Loader()  # Create object to load data from json
        data = loader.importData("../data/mini_json_dataset.json")  # Get data
        handler = dataHandler()  # Create object to handle data
        handler.getTime(data)
        handler.getBreaks(data)  # Get duty times
        Reports.generateFullReport(handler, "../reports")

        assert os.path.exists("../reports/fullReport.csv")  # Check if report was created

if __name__ == '__main__':
    unittest.main()
