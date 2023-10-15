from abc import ABC, abstractmethod
import json
import os


class Saver(ABC):
    @abstractmethod
    def write_file(self):
        pass

    # @abstractmethod
    # def get_info(self):
    #     pass

    @abstractmethod
    def del_info(self):
        pass


class JsonSaver(Saver):

    def __init__(self, vacancies):
        self.vacancies = vacancies

    def write_file(self, file_name):
        '''Записывает информацию в файл'''
        self.file_name = file_name
        with open(self.file_name, 'at') as f:
            json.dump(self.vacancies, f, indent=2)

    def del_info(self):
        '''Удаляет данные из файла'''
        with open(self.file_name, 'wt') as f:
            pass
