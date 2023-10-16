from abc import ABC, abstractmethod
from src.vacancy import Vacancy
import requests


class API(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def change_date(self, new_date):
        pass

    @abstractmethod
    def add_words(self, new_words):
        pass

    @abstractmethod
    def change_area(self, new_area_id):
        pass


class HeadHunter_API(API):
    """Парсинг вакансий на сайте hh.ru"""

    HH_API_URL = 'https://api.hh.ru/vacancies/'
    HH_API_URL_AREAS = 'https://api.hh.ru/suggests/areas'

    @classmethod
    def get_id(cls, town):
        "Получает id города по его названию (нужен для запроса)"
        params = {'text': town}
        responce = requests.get(cls.HH_API_URL_AREAS, params=params)
        areas = responce.json()
        return areas['items'][0]['id']

    def __init__(self, text: str, area_id: int, date: int):
        self.param = {'text': text, 'per_page': 100, 'area': area_id, 'date': date, 'only_with_salary': True}

    def get_vacancies(self):
        """Запрос на получение данных по вакансиям"""
        self.responce = requests.get(self.HH_API_URL, self.param)
        return self.responce.json()['items']

    def create_vacancy(self, vacancies_info):
        """Создает экземпляры класса Vacancy на основе результатов запроса"""
        n = 0
        if len(vacancies_info) == 0:
            print('По вашему запросу вакансии не найдены.')
            Vacancy.all = {}
        else:
            print(f'По Вашему запросу найдено {len(vacancies_info)} вакансий')
            for vac in vacancies_info:
                n += 1
                vacancies_info[n - 1]['number'] = n
                vac_name = vac['name']
                vac_url = vac['alternate_url']
                vac_salary = vac['salary']
                vac_requirement = vac['snippet']['requirement']
                vac_responsibility = vac['snippet']['responsibility']
                vacancy = Vacancy(n, vac_name, vac_url, vac_salary, vac_requirement, vac_responsibility)

    def change_date(self, new_date):
        """Меняет дату в параметрах запроса"""
        self.param['date'] = new_date

    def add_words(self, new_word):
        """Добавляет слова в параметры запроса"""
        self.param['text'] = self.param['text'] + ', ' + new_word

    def change_area(self, new_area_id):
        """Меняет id города в параметрах запроса"""
        self.param['area'] = new_area_id


class SuperJob_API(API):
    """Парсинг вакансий на сайте superjob.ru"""

    SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies/'
    SJ_API_URL_AREAS = 'https://api.superjob.ru/2.0/towns/'
    SJ_API_TOKEN = 'v3.r.10214390.d7472fe3a056fc348b804c5e9fdb189489c069d6.56bc4f8bde07ef965cba0f8cbaeab744d6ffba5d'

    def __init__(self, text: str, area: str, date: int):
        self.param = {'keyword': text, 'count': 100, 'town': area, 'period': date, 'no_agreement': 1}

    def get_vacancies(self):
        """Запрос на получение данных по вакансиям"""
        headers = {'X-Api-App-Id': self.SJ_API_TOKEN}
        responce = requests.get(self.SJ_API_URL, headers=headers, params=self.param)
        return responce.json()['objects']

    def create_vacancy(self, vacancies_info):
        """Создает экземпляры класса Vacancy на основе результатов запроса"""
        n = 0
        if len(vacancies_info) == 0:
            print('По вашему запросу вакансии не найдены.')
            Vacancy.all = {}
        else:
            print(f'По Вашему запросу найдено {len(vacancies_info)} вакансий')
            for vac in vacancies_info:
                n += 1
                vacancies_info[n - 1]['number'] = n
                vac_name = vac['profession']
                vac_url = vac['link']
                vac_salary = {'from': vac['payment_from'], 'to': vac['payment_to'], 'currency': vac['currency']}
                vac_requirement = vac['candidat']
                vacancy = Vacancy(n, vac_name, vac_url, vac_salary, vac_requirement, responsibility=None)

    def change_date(self, new_date):
        """Меняет дату в параметрах запроса"""
        self.param['period'] = new_date

    def add_words(self, new_word):
        """Добавляет слова в параметры запроса"""
        self.param['keyword'] = self.param['keyword'] + ', ' + new_word

    def change_area(self, new_area):
        """Меняет город в параметрах запроса"""
        self.param['town'] = new_area
