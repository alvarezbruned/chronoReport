import os
from tkinter import *
from chrono_item import ChronoItem


class ChronoReport:
    tk = Tk()
    chronos = list()

    item_created_counter = 0
    items_created_in_row = 0
    num_row = 0
    if os.getenv('CHRONO_NAMES', "") != '':
        names = os.getenv('CHRONO_NAMES', "").split("|")
        while item_created_counter < len(names):
            chronos.append(ChronoItem(tk, (items_created_in_row + 1), num_row))
            chronos[item_created_counter].set_name(names[item_created_counter])
            items_created_in_row += 1
            item_created_counter += 1
            if items_created_in_row >= 6:
                items_created_in_row = 0
                num_row += 1
    else:
        while item_created_counter < int(os.getenv('CHRONO_NUM_ITEMS', 3)):
            chronos.append(ChronoItem(tk, (items_created_in_row + 1), num_row))
            chronos[item_created_counter].set_name('item ' + str(item_created_counter))
            items_created_in_row += 1
            item_created_counter += 1
            if items_created_in_row >= 6:
                items_created_in_row = 0
                num_row += 1

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
        with open(os.getenv('CHRONO_PATH_REPORT', 'delay_report.csv'), "w+") as log_file:
            for chrono in self.chronos:
                if chrono.tiempo_reporting != '':
                    name = chrono.get_name()
                    log_file.write('"' + name + '","'
                                   + chrono.tiempo_reporting_start + '","'
                                   + chrono.tiempo_reporting.replace('\n', '","') + '"\n')
                    chrono.tiempo_reporting = ''
                    chrono.tiempo_reporting_start = ''
                    chrono.clean_fields()


app = ChronoReport()
