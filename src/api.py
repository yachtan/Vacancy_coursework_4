from abc import ABC, abstractmethod
import copy
import requests
import json


class API(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def change_date(self):
        pass

    @abstractmethod
    def add_words(self):
        pass

    @abstractmethod
    def add_area(self):
        pass

    # @abstractmethod
    # def load_all_areas(self):
    #     pass


class HeadHunter_API(API):

    HH_API_URL = 'https://api.hh.ru/vacancies/'
    HH_API_URL_AREAS = 'https://api.hh.ru/suggests/areas'

    @classmethod
    def get_id_new(cls, town):
        params = {'text': town}
        responce = requests.get(cls.HH_API_URL_AREAS, params=params)
        areas = responce.json()
        return areas['items'][0]['id']

    def __init__(self, text, area_id, date):
        # self.area_id = HeadHunter_API.get_id_new(area)
        self.param = {'text': text, 'per_page': 100, 'area': area_id, 'date': date, 'only_with_salary': True}

    def get_vacancies(self):
        self.responce = requests.get(self.HH_API_URL, self.param)
        return self.responce.json()['items']

    def change_date(self):
        pass

    def add_words(self):
        pass

    def add_area(self):
        pass



    # @classmethod
    # def load_all_areas(cls):
    #     '''Возвращает словарь, где ключи - это наименования городов (Россия), а значения - id'''
    #     areas = {}
    #     responce = requests.get(cls.HH_API_URL_AREAS)
    #     all_areas = responce.json()
    #     # return all_areas
    #     for country in all_areas:
    #         if country['name'] == 'Россия':
    #             for item in country['areas']:
    #                 areas[item['name']] = item['id']
    #                 for sity in item['areas']:
    #                     # print(f"{sity['id']} это {sity['name']}")
    #                     areas[sity['name']] = sity['id']
    #     return areas
    #
    # @classmethod
    # def get_id(cls, town):
    #     return cls.load_all_areas()[town]




class SuperJob_API(API):
    SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies/'
    SJ_API_URL_AREAS = 'https://api.superjob.ru/2.0/towns/'
    SJ_API_TOKEN = 'v3.r.10214390.d7472fe3a056fc348b804c5e9fdb189489c069d6.56bc4f8bde07ef965cba0f8cbaeab744d6ffba5d'

    param_zero = {'per_page': 100}

    def __init__(self):
        self.param = copy.deepcopy(self.param_zero)

    def get_vacancies(self):
        headers = {'X-Api-App-Id': self.SJ_API_TOKEN}
        responce = requests.get(self.SJ_API_URL, headers=headers, param=self.param)
        return responce.json() #['items']

    def change_date(self):
        pass

    def add_words(self):
        pass

    def add_area(self):
        pass

    def load_all_areas(self):
        responce = requests.get(self.HH_API_URL_AREAS)
        return responce.json()
#     по полученным данным пройтись и вытащить в отдельный словарь имя места и его айди