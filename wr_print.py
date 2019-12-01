#!/usr/bin/python3

import yaml
import requests
import time
from threading import Timer
import logging
logging.basicConfig(level=logging.ERROR)


class WrLinien:
    def __init__(self):
        self.api_key = None
        self.api_url = None
        self.config = self.loadConfig()
        self.response = None

    def loadConfig(self):
        with open("config.yaml", 'r') as stream:
            self.config = yaml.safe_load(stream)
            logging.info('Loading yaml file successful.')
            return self.config

    def setup(self):
        self.api_url = 'https://www.wienerlinien.at/ogd_realtime/monitor?rbl={}&sender={}'.format(self.rbl, self.api_key)
        self.response = requests.get(self.api_url)
        try:
            self.response.raise_for_status()					# Check if HTTP response code is 200.print(response)
            return self.response
        except requests.exceptions.HTTPError as ex: 	# If not, throw a exception and print the error message.
            logging.warning(ex)

    def requestData(self):
        output = []
        try:
            for i in range(0, 2):
                monitor = self.response.json()['data']['monitors'][0]
                line = monitor['lines'][0]
                name = line['name']
                direction = line['towards']
                time = line['departures']['departure'][i]['departureTime']['countdown']
                if time is 0:
                    time = '*'
                output.append("{} {:<20} {:>4}".format(name, direction, time))
            return print('\n'.join(output))
        except:
            logging.error("Something went wrong while extracting the required data. Try again...")

    def doQuery(self):
        for element in self.config['rbl']:
            wrLinien.rbl = self.config['rbl'][element]
            wrLinien.api_key = self.config['keys']['test_key']
            wrLinien.setup()
            wrLinien.requestData()
        print()


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


if __name__ == '__main__':
    wrLinien = WrLinien()

    refresh_time = 1
    timer = RepeatTimer(refresh_time, wrLinien.doQuery)
    timer.start()