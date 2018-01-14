from elastic_dao import Elastic_DAO


class DAO_Factory:

    @staticmethod
    def get_dao(db_name):
        if db_name == 'Elasticsearch':
            return Elastic_DAO()
