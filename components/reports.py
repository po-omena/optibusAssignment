import pandas as pd
import os


class Reports:

    @staticmethod
    def generateTimeReport(handler, path):
        df = handler.times
        print(df)
        df.to_csv(os.path.join(path, "timeReport.csv"), index=False)
        print("Report generated successfully")
        return df

    @staticmethod
    def generateBreakReport(handler, path):
        df = handler.breaks
        print(df)
        df.to_csv(os.path.join(path, "breakReport.csv"), index=False)
        print("Report generated successfully")
        return df

    @staticmethod
    def generateFullReport(handler, path):
        times = handler.times
        breaks = handler.breaks
        filteredBreaks = breaks.loc[breaks['Duty ID'].isin(times['Duty ID']) & (breaks['Break Duration'] >= 15)]
        df = pd.merge(times, filteredBreaks, on=['Duty ID', 'Duty ID'])
        print(df)
        df.to_csv(os.path.join(path, "fullReport.csv"), index=False)
        print("Report generated successfully")
        return df
