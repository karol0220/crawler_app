import os
import json
import threading
import logging

from elasticsearch import Elasticsearch
from elasticsearch import ElasticsearchException
import yaml

from dao import DAO


class Elastic_DAO(DAO):
    def __init__(self):
        self.lock = threading.Lock()

        config = self._read_config()
        self.client = Elasticsearch(hosts=config['elastic']['hosts'])
        self.queries = self._read_queries()

        self._create_index_and_mapping_if_not_exist()

    def save_response(self, url, resp_code, elapsed_seconds, date_time):
        with self.lock:
            document = json.dumps({
                "url": url,
                "resp_code": resp_code,
                "elapsed_time": elapsed_seconds,
                "timestamp": date_time
            }, ensure_ascii=False)
            try:
                self.client.index(index='responses', doc_type='response', body=document)
            except ElasticsearchException:
                logging.exception('Cannot connect to ElasticSearch')

    def get_all_responses(self):
        with self.lock:
            query = json.dumps(self.queries['search_all'])
            return self._get_response(query)

    def get_service_responses(self, service):
        with self.lock:
            query = json.dumps(self.queries['search_service']) % service
            return self._get_response(query)

    def get_code_responses(self, code):
        with self.lock:
            query = json.dumps(self.queries['search_code']) % code
            return self._get_response(query)

    def close_connection(self):
        try:
            self.client.transport.close()
        except ElasticsearchException:
            logging.exception('Cannot connect to ElasticSearch')

    def _get_response(self, query):
        response = []
        try:
            elastic_response = self.client.search(index='responses', body=query)
        except ElasticsearchException:
            logging.exception('Cannot connect to ElasticSearch')
        else:
            for document in elastic_response['hits']['hits']:
                response.append(document['_source'])
        return response

    def _create_index_and_mapping_if_not_exist(self):
        try:
            if not self.client.indices.exists(index='responses'):
                self.client.indices.create(index='responses')
                mapping = json.dumps(self.queries['mapping'])
                self.client.indices.put_mapping(index='responses', doc_type='response', body=mapping)
        except ElasticsearchException:
            logging.exception('Cannot connect to ElasticSearch')

    @staticmethod
    def _read_config():
        path = os.path.join(os.path.dirname(__file__), 'config', 'db_config.yml')
        with open(path) as file:
            return yaml.load(file)

    @staticmethod
    def _read_queries():
        path = os.path.join(os.path.dirname(__file__), 'config', 'queries.json')
        with open(path) as file:
            return json.load(file)
