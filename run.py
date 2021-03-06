#!/usr/bin/python3

import yaml
import requests
import json
import logging
import time
import random
from threading import Timer
logging.basicConfig(level=logging.INFO)

class WrLinien:
    def __init__(self):
        self.api_url = None
        self.config = self.loadConfig()
        self.response = None
        self.dataOut = {}
        self.batchnumber = 0
        self.stopcount = 0
        self.excount = 0

    def loadConfig(self):
        with open("config.yaml", 'r') as stream:
            self.config = yaml.safe_load(stream)
            logging.info('Loading yaml file successful.')
            return self.config

    def requestData(self):
        self.api_url = 'https://www.wienerlinien.at/ogd_realtime/monitor?rbl={}'.format(self.rbl)
        try:
            self.response = requests.get(self.api_url, timeout=15)
        except Exception as ex:
            self.excount += 1
            return logging.exception(ex)
        self.response.raise_for_status()
        self.dataOut[self.rbl] = self.response.json()
        self.stopcount += 1

    def saveData(self):
        path = self.config['paths']['data_storage']
        filename = time.strftime("%Y%m%d_%H%M%S")
        try:
            with open(path + filename, 'w') as outfile:
                json.dump(self.dataOut, outfile)
        except Exception:
            self.excount += 1
            logging.debug("Something went wrong while trying to save file {}".format(filename))

    def doParsing(self):
        wrLinien.resetCount()
        self.dataOut.clear()
        for line, stops in self.config['rbl'].items():
            random.shuffle(stops)
            for i in stops:
                wrLinien.rbl = i
                wrLinien.requestData()
        wrLinien.saveData()
        self.batchnumber += 1
        logging.info("Completed batch #{} at {} for {} stops causing {} exception(s)".format(self.batchnumber,
                                                                                             time.strftime("%Y%m%d_%H%M%S"),
                                                                                             self.stopcount,
                                                                                             self.excount))

    def resetCount(self):
        self.stopcount = 0
        self.excount = 0


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


if __name__ == '__main__':
    wrLinien = WrLinien()

    refresh_time = 60
    timer = RepeatTimer(refresh_time, wrLinien.doParsing)
    timer.start()