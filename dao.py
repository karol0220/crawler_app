from abc import ABC, abstractmethod


class DAO(ABC):
    @abstractmethod
    def save_response(self, url, resp_code, elapsed_time, date_time):
        pass

    @abstractmethod
    def get_all_responses(self):
        pass

    @abstractmethod
    def get_service_responses(self, service):
        pass

    @abstractmethod
    def get_code_responses(self, code):
        pass

    @abstractmethod
    def close_connection(self):
        pass
