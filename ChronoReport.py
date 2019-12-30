import os
from tkinter import *
import datetime
import time
from ChronoItem import ChronoItem


class ChronoReport:
    tk = Tk()
    chronos = list()
    for x in range(0, os.getenv('CHRONO_NUM_ITEMS', 6)):
        chronos.append(ChronoItem(tk, (x + 1)))

    def __init__(self):
        self.reporting = Button(self.tk)
        self.reporting["text"] = "reporting"
        self.reporting["command"] = lambda: self.report_times()
        self.reporting.grid(column=0, row=0)

        self.update_labels()
        self.tk.mainloop()

    def update_labels(self):
        for chrono in self.chronos:
            chrono.update_labels()

    def report_times(self):
        for chrono in self.chronos:
            if chrono.tiempo_reporting != '':
                name = chrono.get_name()
                os.popen('echo "'
                         + name + ' '
                         + chrono.tiempo_reporting_start
                         + ' '
                         + chrono.tiempo_reporting +
                         '" >> ' + os.getenv('CHRONO_PATH_REPORT', '~/delay_report.txt'))
                chrono.tiempo_reporting = ''
                chrono.tiempo_reporting_start = ''
                chrono.clean_fields()

app = ChronoReport()
