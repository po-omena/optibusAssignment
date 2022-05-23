import warnings
from components.loader import Loader
from components.reports import Reports
from components.dataHandler import dataHandler

loader = Loader()  # Create object to load data from json
data = loader.importData("./data/mini_json_dataset.json")  # Get data
handler = dataHandler()  # Create object to handle data
handler.getTime(data)  # Get duty times
handler.getBreaks(data)  # Get duty breaks
Reports.generateFullReport(handler, "./reports")  # Get full report

