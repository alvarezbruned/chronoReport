from tkinter import *
import datetime
import time


class ChronoItem():
    time_init = 0
    time_end = 0
    tiempo_reporting_start = ""
    tiempo_reporting = ""
    pos = 0


    def label_builder(self, tk, action):
        label = Label(tk)
        if action == 'start':
            label["text"] = str(self.tiempo_reporting_start)
        else:
            label["text"] = str(self.tiempo_reporting)
        return label

    def button_builder(self, tk, action):
        button = Button(tk)
        button["text"] = action
        if action == 'start':
            button["command"] = lambda: self.start_time()
        else:
            button["command"] = lambda: self.final_time_action()
        return button

    def start_time(self):
        self.time_init = time.time()
        self.tiempo_reporting_start = self.actual_datetime()
        print(self.get_name() + ' ' + self.tiempo_reporting_start)
        self.label_start["text"] = self.tiempo_reporting_start
        self.tiempo_reporting = ''
        return self.time_init

    def final_time_action(self):
        if self.tiempo_reporting_start == '':
            return None
        self.time_end = time.time()
        tiempo_transcurrido = self.time_end - self.time_init

        todaySufix = self.actual_datetime()

        self.tiempo_reporting = todaySufix + '  ' + self.secondsToDateFormat(tiempo_transcurrido)
        print(self.get_name() + ' ' + self.tiempo_reporting)

        self.label_stop["text"] = self.tiempo_reporting

        return self.tiempo_reporting

    def actual_datetime(self):
        now = datetime.datetime.now()
        todaySufix = str(now.day) \
                     + '/' + str(now.month) \
                     + '/' + str(now.year) \
                     + ' ' + str(now.hour) \
                     + ':' + str(now.minute) \
                     + ':' + str(now.second)
        return todaySufix

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

    def __init__(self, tk, pos):
        self.pos = pos
        self.name = Entry(tk)
        self.button_start = self.button_builder(tk, 'start')
        self.button_stop = self.button_builder(tk, 'stop')
        self.label_start = self.label_builder(tk, 'start')
        self.label_stop = self.label_builder(tk, 'stop')
        self.organize_components(pos)

    def organize_components(self, pos):
        self.name.grid(column=pos, row=0)
        self.button_start.grid(column=pos, row=1)
        self.button_stop.grid(column=pos, row=2)
        self.label_start.grid(column=pos, row=4)
        self.label_stop.grid(column=pos, row=5)

    def clean_fields(self):
        self.label_start["text"] = ''
        self.label_stop["text"] = ''

    def update_labels(self):
        self.label_start["text"] = self.tiempo_reporting_start
        if self.tiempo_reporting_start != '' and self.tiempo_reporting == '':
            self.label_stop["text"] = self.refreshTimeLapsed(self.time_init)
        else:
            self.label_stop["text"] = self.tiempo_reporting
        self.label_stop.after(1000, self.update_labels)

    def refreshTimeLapsed(self, time_initial):
        actual_time = time.time()
        tiempo_lapsed = actual_time - time_initial
        return self.secondsToDateFormat(tiempo_lapsed)

    def get_name(self):
        return 'item ' + str(self.pos) if self.name.get() == '' else self.name.get()
