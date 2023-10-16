class Vacancy:
    """Класс для работы с вакансиями"""

    all = {}

    def __init__(self, n, name, url, salary, requirement, responsibility):
        self.number = n
        self.name = name
        self.url = url
        self.salary = salary
        self.requirement = requirement
        self.responsibility = responsibility
        Vacancy.all[self.number] = self

    def __str__(self):
        return f'Вакансия № {self.number}. {self.name}'

    def __sub__(self, other):
        """Позволяет получать разницу ЗП у вакансий (по нижней границе, если указан диапазон)"""

        if isinstance(other, Vacancy):
            if self.salary['currency'] == 'RUR' and other.salary['currency'] == 'RUR':
                return int(self.salary['from']) - int(other.salary['from'])
            elif self.salary['currency'] == 'rub' and other.salary['currency'] == 'rub':
                return int(self.salary['from']) - int(other.salary['from'])
            else:
                print('Нельзя получить разницу, т.к. зарплата указана не в рублях!')
        else:
            raise Exception('Нельзя вычитать данные элементы!')

    @classmethod
    def get_max(cls):
        """Показывает вакансии с максимальной ЗП из всех"""

        all_salaries = {}

        for v in Vacancy.all.values():
            if v.salary['from'] != None:
                all_salaries[v.number] = int(v.salary['from'])
            else:
                all_salaries[v.number] = int(v.salary['to'])

        max_salary = max(all_salaries.values())
        max_list = list(k for k, v in all_salaries.items() if v == max_salary)
        print(f'Вакансии с максимальной зарплатой {max_salary} рублей: номер {max_list}')
        print('Информация по данным вакансиям:')
        for m in max_list:
            Vacancy.all[m].print_info()

    def print_info(self):
        "Выводит информацию о вакансии для пользователя"
        print(f'{self.number}. {self.name}:\n'
              f'Ссылка: {self.url}\n'
              f'Требования: {self.requirement}')

        if self.responsibility == None:
            print('Обязанности: не указано')
        else:
            print(f'Обязанности: {self.responsibility}')

        if self.salary["to"] == None:
            print(f'Зарплата: {self.salary["from"]} рублей\n')
        elif self.salary["from"] == None:
            print(f'Зарплата: до {self.salary["to"]} рублей\n')
        else:
            print(f'Зарплата: от {self.salary["from"]} до {self.salary["to"]} рублей\n')

    @classmethod
    def print_info_all(cls):
        "Выводит информацию о всех вакансиях для пользователя"
        print(f'Вакансии:\n')
        for vac in Vacancy.all.values():
            vac.print_info()
