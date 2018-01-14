import sys
import os

import yaml

from dao_factory import DAO_Factory
from requester import Requester


class Main:
    def __init__(self):
        self.threads = []
        self.app_config = self._get_app_config()
        self.urls_config = self._get_urls_config()
        self.dao = DAO_Factory().get_dao(self.app_config['database'])

    def run(self):
        try:
            self._run_requesters()
            while True:
                pass
        except KeyboardInterrupt:
            for t in self.threads:
                t.stop_processing = True
            for t in self.threads:
                t.join()
            self.dao.close_connection()
            sys.exit(0)

    def _run_requesters(self):
        for service in self.urls_config['urls']:
            t = Requester(service['url'], service['delay'], self.dao)
            self.threads.append(t)
            t.start()

    @staticmethod
    def _get_app_config():
        app_config_path = os.path.join(os.path.dirname(__file__), "config", "app_config.yml")
        with open(app_config_path) as file:
            return yaml.load(file)

    @staticmethod
    def _get_urls_config():
        config_path = os.path.join(os.path.dirname(__file__), "config", "urls.yml")
        with open(config_path) as file:
            return yaml.load(file)


if __name__ == '__main__':
    Main().run()
