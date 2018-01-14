import threading
import logging
from time import sleep
from datetime import datetime

import requests


class Requester(threading.Thread):
    def __init__(self, url, delay, dao):
        super().__init__()

        self.dao = dao
        self.url = url
        self.delay = delay
        self.stop_processing = False

    def run(self):
        while not self.stop_processing:
            try:
                sleep(int(self.delay))
                if self.stop_processing:
                    break
            except InterruptedError:
                logging.exception(str(threading.current_thread()) + ' interrupted')

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            response = self._request()
            if response:
                self._save_response(response, timestamp)


    def _request(self):
        response = None
        try:
            response = requests.get(self.url)
        except requests.ConnectionError:
            logging.exception('Requester Connection Exception')
        return response

    def _save_response(self, response, timestamp):
        resp_code = response.status_code
        elapsed_seconds = response.elapsed.total_seconds()
        self.dao.save_response(self.url, resp_code, elapsed_seconds, timestamp)