import os
from tkinter import *
import datetime
import time

class ChronoReport(Frame):
    time_init = [0, 0, 0]
    time_end = [0, 0, 0]
    tiempo_reporting_start = ["", "", ""]
    tiempo_reporting = ["", "", ""]

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.grid(column=3, row=1)

        self.first_name = Entry(self)
        self.first_name.grid(row=0, column=0)

        self.second_name = Entry(self)
        self.second_name.grid(row=0, column=1)

        self.third_name = Entry(self)
        self.third_name.grid(row=0, column=2)

        self.first_start = self.button_builder(0, 'start')
        self.first_stop = self.button_builder(0, 'stop')
        self.l_first_start = self.label_builder(0, 'start')
        self.l_first_stop = self.label_builder(0, 'stop')

        self.second_start = self.button_builder(1, 'start')
        self.second_stop = self.button_builder(1, 'stop')
        self.l_second_start = self.label_builder(1, 'start')
        self.l_second_stop = self.label_builder(1, 'stop')

        self.third_start = self.button_builder(2, 'start')
        self.third_stop = self.button_builder(2, 'stop')
        self.l_third_start = self.label_builder(2, 'start')
        self.l_third_stop = self.label_builder(2, 'stop')

        self.reporting = Button(self)
        self.reporting["text"] = "reporting"
        self.reporting["command"] = self.report_times
        self.reporting.grid(column=3, row=0)

        self.update_labels()

    def label_builder(self, pos, action):
        label = Label(self)
        if action == 'start':
            label["text"] = str(self.tiempo_reporting_start[pos])
            label.grid(column=pos, row=4)
        else:
            label["text"] = str(self.tiempo_reporting[pos])
            label.grid(column=pos, row=5)
        return label

    def button_builder(self, pos, action):
        button = Button(self)
        button["text"] = action
        if action == 'start':
            button["command"] = lambda: self.start_time(pos)
            button.grid(column=pos, row=1)
        else:
            button["command"] = lambda: self.final_time_action(pos)
            button.grid(column=pos, row=2)
        return button

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def start_time(self, pos):
        self.time_init[pos] = time.time()
        self.tiempo_reporting_start[pos] = self.actual_datetime()
        print(self.tiempo_reporting_start[pos])
        if pos == 0:
            self.l_first_start["text"] = self.tiempo_reporting_start[pos]
        if pos == 1:
            self.l_second_start["text"] = self.tiempo_reporting_start[pos]
        if pos == 2:
            self.l_third_start["text"] = self.tiempo_reporting_start[pos]
        return self.time_init[pos]

    def final_time_action(self, pos):
        if self.tiempo_reporting_start[pos] == '':
            return None
        self.time_end[pos] = time.time()
        tiempo_transcurrido = self.time_end[pos] - self.time_init[pos]

        todaySufix = self.actual_datetime()

        self.tiempo_reporting[pos] = todaySufix + '  ' + self.secondsToDateFormat(tiempo_transcurrido)
        print(self.tiempo_reporting[pos])
        if pos == 0:
            self.l_first_stop["text"] = self.tiempo_reporting[pos]
        if pos == 1:
            self.l_second_stop["text"] = self.tiempo_reporting[pos]
        if pos == 2:
            self.l_third_stop["text"] = self.tiempo_reporting[pos]

        return self.tiempo_reporting[pos]

    def actual_datetime(self):
        now = datetime.datetime.now()
        todaySufix = str(now.day) \
                     + '/' + str(now.month) \
                     + '/' + str(now.year) \
                     + ' ' + str(now.hour) \
                     + ':' + str(now.minute) \
                     + ':' + str(now.second)
        return todaySufix

    def refreshTimeLapsed(self, time_initial):
        actual_time = time.time()
        tiempo_lapsed = actual_time - time_initial
        return self.secondsToDateFormat(tiempo_lapsed)

    def update_labels(self):
        self.l_first_start["text"] = self.tiempo_reporting_start[0]
        self.l_second_start["text"] = self.tiempo_reporting_start[1]
        if self.tiempo_reporting_start[0] != '' and self.tiempo_reporting[0] == '':
            self.l_first_stop["text"] = self.refreshTimeLapsed(self.time_init[0])
        else:
            self.l_first_stop["text"] = self.tiempo_reporting[0]

        if self.tiempo_reporting_start[1] != '' and self.tiempo_reporting[1] == '':
            self.l_second_stop["text"] = self.refreshTimeLapsed(self.time_init[1])
        else:
            self.l_second_stop["text"] = self.tiempo_reporting[1]

        if self.tiempo_reporting_start[2] != '' and self.tiempo_reporting[2] == '':
            self.l_third_stop["text"] = self.refreshTimeLapsed(self.time_init[2])
        else:
            self.l_third_stop["text"] = self.tiempo_reporting[2]
        self.after(1000, self.update_labels)

    def secondsToDateFormat(self, tiempo_transcurrido):
        seconds = tiempo_transcurrido
        minutes = seconds / 60
        if minutes == 0:
            hours = 0
        else:
            hours = minutes / 60
        if seconds > 60:
            seconds = (seconds % 60)
        if minutes > 60:
            minutes = (minutes % 60)
        if hours < 10:
            hours = "0%s" % str(int(hours))
        else:
            hours = "%s" % str(int(hours))
        if minutes < 10:
            minutes = "0%s" % str(int(minutes))
        else:
            minutes = "%s" % str(int(minutes))
        if seconds < 10:
            seconds = "0%s" % str(int(seconds))
        else:
            seconds = "%s" % str(int(seconds))
        time_passed = "%sh %sm %ss" % (hours, minutes, seconds)
        return time_passed

    def report_times(self):
        cursor = 0
        for x in self.tiempo_reporting:
            if x != '':
                name = self.reported_name(cursor)
                os.popen('echo "'
                         + name + ' '
                         + self.tiempo_reporting_start[cursor]
                         + ' '
                         + self.tiempo_reporting[cursor] +
                         '" >> ~/reporte_delays.txt')
                self.tiempo_reporting[cursor] = ''
                self.tiempo_reporting_start[cursor] = ''
                self.clean_fields(cursor)
            cursor += 1

    def clean_fields(self, cursor):
        if cursor == 0:
            self.l_first_start["text"] = ''
            self.l_first_stop["text"] = ''
        elif cursor == 1:
            self.l_second_start["text"] = ''
            self.l_second_stop["text"] = ''
        elif cursor == 2:
            self.l_third_start["text"] = ''
            self.l_third_stop["text"] = ''

    def reported_name(self, cursor):
        if cursor == 0:
            name = 'first' if self.first_name.get() == '' else self.first_name.get()
        elif cursor == 1:
            name = 'second' if self.second_name.get() == '' else self.second_name.get()
        elif cursor == 2:
            name = 'third' if self.third_name.get() == '' else self.third_name.get()
        return name


root = Tk()
app = ChronoReport(master=root)
app.mainloop()
root.destroy()
